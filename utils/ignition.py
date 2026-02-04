import base64
import gzip
import json
from utils.datatypes import FileContents, FileEntry, Ignition, IgnitionConfig, StorageFiles, SystemdUnits, kernelArguments


def empty_ignition(version: str = "3.4.0") -> Ignition:
    return Ignition(
        ignition=IgnitionConfig(
            version=version,
            config={},
        ),
        storage=StorageFiles(
            files=[],
        ),
        systemd=SystemdUnits(
            units=[],
        ),
        kernelArguments=kernelArguments(
            shouldExist=[],
            shouldNotExist=[],
        ),
    )


def encode_ignition(ign: Ignition) -> str:
    """
    Encodes the ignition file to base64.
    Args:
        ign: The ignition file content
    Returns:
        str: The base64 encoded ignition file
    """
    # Encode the ignition file to base64
    gzipped_ign = gzip.compress(json.dumps(
        ign, separators=(',', ':')).encode('utf-8'))
    return base64.b64encode(gzipped_ign).decode()


def encode_gz_compress_file(file: FileContents) -> FileContents:

    # check if binary or text

    # Text
    if isinstance(file['source'], str):
        source = file['source'].encode()
    else:
        source = file['source']

    return {
        "compression": "gzip",
        "source": f"data:;base64,{base64.b64encode(gzip.compress(source)).decode()}"
    }
