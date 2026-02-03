#!/usr/bin/python3

import argparse
import json
import os
import sys
import traceback
from pathlib import Path

from special.machineos import replace_machine_os_url
from special.mtu9000 import mtu9000_enable
from special.ovs_script import add_flavor_ovs_script
from utils.content import add_files, add_systemd_units
from utils.datatypes import Ignition
from utils.ignition import empty_ignition, encode_ignition
from utils.oc import create_bfb_template_cm, get_flavor, pull_ignition

TARGET_CONTENT_DIR = Path(__file__).parent / "content" / "target"
LIVE_CONTENT_DIR = Path(__file__).parent / "content" / "live"


def argparse_setup() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate OpenShift/DPF ignition template')
    parser.add_argument('--flavor', type=str, required=True,
                        help='Flavor to use')
    parser.add_argument('--mtu9000', action='store_true',
                        help='Enable MTU 9000 configuration')
    parser.add_argument('--machine-os-url', type=str, required=True,
                        help='Machine OS URL')
    parser.add_argument('--cluster', '-c', type=str, default='doca',
                        help='Name of the cluster to pull ignition from')
    parser.add_argument('--hosted-clusters-namespace', '-hc', type=str, default='clusters',
                        help='Namespace for hosted clusters (default: clusters)')
    parser.add_argument('--output-file', '-f', type=str,
                        default='hcp_template.yaml',)
    # debug ignition file,  boolean
    parser.add_argument('--debug-ignition', action='store_true',
                        help='Debug ignition file')
    return parser.parse_args()


def main():
    args = argparse_setup()

    # Check KUBECONFIG environment variable
    kubeconfig = os.environ.get('KUBECONFIG')
    if not kubeconfig:
        print("KUBECONFIG environment variable is not set.")
        return
    print(f"KUBECONFIG: {kubeconfig}")

    target_ignition: Ignition = pull_ignition(
        args.cluster, args.hosted_clusters_namespace)

    dpu_flavor = get_flavor(args.flavor)

    replace_machine_os_url(target_ignition, args.machine_os_url)

    add_files(target_ignition, TARGET_CONTENT_DIR)
    add_systemd_units(target_ignition, TARGET_CONTENT_DIR)
    add_flavor_ovs_script(target_ignition, dpu_flavor)

    if args.mtu9000:
        print("Enabling MTU 9000 configuration.")
        mtu9000_enable(target_ignition)

    encoded_ign = encode_ignition(target_ignition)

    ign = empty_ignition()

    # Copy target ignition passwd to live ignition
    ign['passwd'] = target_ignition['passwd'].copy()

    add_files(ign, LIVE_CONTENT_DIR)
    add_systemd_units(ign, LIVE_CONTENT_DIR)

    ign['storage']['files'].append({
        'path': '/var/target.ign',
        'contents': {
            "compression": "gzip",
            "source": f"data:;base64,{encoded_ign}"
        }
    })

    create_bfb_template_cm(ign, args.output_file)
    # save formatted json to file

    if args.debug_ignition:
        with open('target.ign', 'w') as f:
            json.dump(target_ignition, f, indent=4)
        with open('output.ign', 'w') as f:
            json.dump(ign, f, indent=4)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exception(sys.exception())
        exit(1)
