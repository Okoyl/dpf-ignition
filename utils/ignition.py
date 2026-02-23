import base64
import gzip
import json
from utils.datatypes import FileContents, FileEntry, Ignition, IgnitionConfig, StorageFiles, SystemdUnits, KernelArguments


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
        kernelArguments=KernelArguments(
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


def gzip_ignition_files(ign: Ignition) -> None:
    """
    Gzip-compress all uncompressed files in an ignition's storage.
    Files that already have compression set are left as-is.
    """
    for file_entry in ign.get('storage', {}).get('files', []):
        contents = file_entry.get('contents', {})
        if contents.get('compression'):
            continue

        source = contents.get('source', '')
        if not source:
            continue

        # Decode the data URL to raw bytes
        if source.startswith('data:,'):
            # URL-encoded inline content
            from urllib.parse import unquote
            raw = unquote(source[len('data:,'):]).encode('utf-8')
        elif ';base64,' in source:
            # Base64-encoded content (e.g. data:;base64,... or data:text/plain;...;base64,...)
            b64_data = source.split(';base64,', 1)[1]
            raw = base64.b64decode(b64_data)
        else:
            continue

        contents['compression'] = 'gzip'
        contents['source'] = f"data:;base64,{base64.b64encode(gzip.compress(raw)).decode()}"


def encode_gz_compress_file(file: FileContents) -> FileContents:
    if isinstance(file['source'], str):
        source = file['source'].encode()
    else:
        source = file['source']

    return {
        "compression": "gzip",
        "source": f"data:;base64,{base64.b64encode(gzip.compress(source)).decode()}"
    }
