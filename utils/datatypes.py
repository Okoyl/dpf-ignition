from typing import Optional, TypedDict

##
# Ignition
##


class FileContents(TypedDict):
    # inline: Optional[str]
    source: Optional[str]


class FileEntry(TypedDict):
    path: str
    overwrite: bool
    mode: int
    contents: FileContents


class SystemdUnit(TypedDict):
    name: str
    enabled: bool
    contents: Optional[str]


class IgnitionConfig(TypedDict):
    version: str
    config: dict


class StorageFiles(TypedDict):
    files: list[FileEntry]


class SystemdUnits(TypedDict):
    units: list[SystemdUnit]


class kernelArguments(TypedDict):
    shouldExist: list[str]
    shouldNotExist: list[str]


class Ignition(TypedDict):
    ignition: IgnitionConfig
    storage: StorageFiles
    systemd: SystemdUnits
    kernelArguments: kernelArguments

##
# Flavor
##


class Grub(TypedDict):
    kernelParameters: list[str]


class NVConfig(TypedDict):
    device: str
    parameters: list[str]


class OVS(TypedDict):
    rawConfigScript: str


class Flavor(TypedDict):
    bfcfgParameters: list[str]
    grub: Grub
    nvconfig: list[NVConfig]
    ovs: OVS
