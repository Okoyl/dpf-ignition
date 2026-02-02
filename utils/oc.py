import http.client
import json
import os
import ssl
import subprocess
from pathlib import Path

from utils.datatypes import Flavor, Ignition

CACHE_DIR = Path("cache")


def execute_oc_command(namespace: str, command: list[str]) -> str:
    """
    Executes an oc command in the specified namespace.
    Args:
        namespace: The namespace to execute the command in
        command: The oc command to execute (without the -n parameter)
    Returns:
        str: The command output
    """
    try:
        return subprocess.check_output(
            ["oc", "-n", namespace] + command
        ).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing oc command: {e}")
        raise


def get_ignition_token_secret(cluster_name: str, namespace: str) -> str:
    # Get token secrets
    ignition_token_secrets = execute_oc_command(
        namespace,
        ["get", "secret", "--no-headers", "-o",
            "custom-columns=NAME:.metadata.name"]
    )

    # Find token-doca secret
    secrets: list[str] = [line for line in ignition_token_secrets.splitlines(
    ) if f"token-{cluster_name}" in line]
    if not secrets:
        raise Exception("No token secrets found.")
    ignition_token_secret: str = secrets[0]

    # Get ignition token
    ignition_token = execute_oc_command(
        namespace,
        ["get", "secret", ignition_token_secret,
            "-o", "jsonpath={.data.token}"]
    )
    return ignition_token


def pull_ignition(cluster_name: str, hc_namespace: str) -> dict:
    """
    Pulls the ignition file from the cluster and caches it.
    If cached file exists, returns cached content instead of pulling.
    Args:
        cluster_name: The name of the cluster to pull ignition from
        hc_namespace: The namespace for hosted clusters
    Returns:
        dict: The ignition file content
    """
    # Check cache first
    cache_file = CACHE_DIR / f"{cluster_name}.ign"
    if cache_file.exists():
        print(f"Using cached ignition file: {cache_file}")
        with open(cache_file, "r") as f:
            return json.load(f)

    print("Pulling ignition file from cluster...")
    namespace = f"{hc_namespace}-{cluster_name}"

    try:
        # Get ignition endpoint
        ignition_endpoint = execute_oc_command(
            hc_namespace,
            ["get", "hc", cluster_name, "-o",
                "jsonpath={.status.ignitionEndpoint}"]
        )
        ignition_token = get_ignition_token_secret(cluster_name, namespace)

        # Download ignition file
        conn = http.client.HTTPSConnection(
            ignition_endpoint, context=ssl._create_unverified_context())
        conn.request("GET", "/ignition",
                     headers={"Authorization": f"Bearer {ignition_token}"})
        response = conn.getresponse()
        if response.status != 200:
            raise Exception(
                f"Failed to pull ignition file: {response.status} {response.reason}")
        data = response.read()
        ignition_data = json.loads(data.decode('utf-8'))

        # Save to cache
        CACHE_DIR.mkdir(exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(ignition_data, f)
        print(f"Downloaded and cached ignition file: {cache_file}")

        return ignition_data

    except Exception as e:
        print(f"Error pulling ignition file: {e}")
        raise


def create_bfb_template_cm(ign: Ignition, configmap_path: str) -> None:
    """Write ConfigMap to disk."""
    # Create ignition template
    ignition_template = json.dumps(ign, separators=(',', ':'))

    # Create ConfigMap
    yaml = """apiVersion: v1
kind: ConfigMap
metadata:
  name: custom-bfb.cfg
  namespace: dpf-operator-system
data:
    BF_CFG_TEMPLATE: |
        """ + ignition_template

    with open(configmap_path, "w") as f:
        f.write(yaml)
    print(f"ConfigMap written to: {configmap_path}")


def get_flavor(flavor_name: str) -> Flavor:
    """
    Gets DPUFlavor from the cluster
    Args:
        flavor_name: The name of the flavor to get
    Returns:
        Flavor: The flavor content
    """
    # Get DPUFlavor
    dpu_flavor = execute_oc_command(
        "dpf-operator-system",
        ["get", "dpuflavors.provisioning.dpu.nvidia.com", flavor_name, "-o", "json"]
    )
    return Flavor(**json.loads(dpu_flavor)['spec'])
