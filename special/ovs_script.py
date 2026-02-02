import base64
from dataclasses import asdict
from utils.datatypes import FileContents, FileEntry, Flavor, Ignition
from utils.misc import octal_to_decimal


def add_flavor_ovs_script(ign: Ignition, flavor: Flavor):
    """
    Inserts the DPU Flavor OVS script into the ignition file.
    """

    ovs_script = flavor['ovs']['rawConfigScript']

    file: FileEntry = FileEntry(
        path="/usr/local/bin/dpf-ovs-script.sh",
        overwrite=True,
        mode=octal_to_decimal(755),
        contents=FileContents(
            source="data:text/plain;charset=utf-8;base64," +
            base64.b64encode(ovs_script.encode()).decode()
        )
    )

    ign['storage']['files'].append(file)
