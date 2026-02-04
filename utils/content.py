import base64
import importlib
from pathlib import Path
from utils.datatypes import FileContents, FileEntry, Ignition, SystemdUnit
from utils.ignition import encode_gz_compress_file
from utils.misc import octal_to_decimal


def _load_from_module(content_dir: Path, attr_name: str):
    """Helper to dynamically import and get an attribute from a content module."""
    module_name = f"content.{content_dir.name}.index"
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)


def load_files(content_dir: Path) -> list[FileEntry]:
    """Load file definitions from a content module and create FileEntry objects."""
    file_defs = _load_from_module(content_dir, "FILES")

    files: list[FileEntry] = []
    files_dir = content_dir / "files"

    for target_path, mode, content_source in file_defs:
        if content_source.startswith("data:"):
            files.append(FileEntry(
                path=target_path,
                overwrite=True,
                mode=octal_to_decimal(mode),
                contents=FileContents(source=content_source)
            ))
        else:
            content_path = files_dir / content_source

            content = FileContents(source=content_path.read_bytes())

            encoded_contents: FileContents = encode_gz_compress_file(content)

            files.append(FileEntry(
                path=target_path,
                overwrite=True,
                mode=octal_to_decimal(mode),
                contents=encoded_contents
            ))

    return files


def load_systemd_units(content_dir: Path) -> list[SystemdUnit]:
    """Load systemd unit files from the systemd directory using glob."""
    units_dir = content_dir / "systemd"

    units: list[SystemdUnit] = []
    for unit_file in sorted(units_dir.glob("*")):
        if unit_file.is_file():
            units.append(SystemdUnit(
                name=unit_file.name,
                enabled=True,
                contents=unit_file.read_text()
            ))

    return units


def add_kernel_args(ign: Ignition) -> None:
    """
    Adds kernel arguments templating to the ignition file.
    """
    ign['kernelArguments'] = {
        'shouldExist': [
            "{{.KernelParameters}}"
        ]
    }


def add_files(ign: Ignition, path: Path) -> None:
    """
    Adds files to the ignition file by dynamically loading from the content module.
    """
    files = load_files(path)

    ign['storage']['files'].extend(files)


def add_systemd_units(ign: Ignition, path: Path) -> None:
    """
    Adds systemd units to the ignition file by dynamically loading from the content module.
    """
    units = load_systemd_units(path)

    for unit in units:
        ign['systemd']['units'].append({
            'name': unit['name'],
            'enabled': unit['enabled'],
            'contents': unit['contents']
        })
