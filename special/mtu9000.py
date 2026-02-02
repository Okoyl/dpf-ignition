from utils.datatypes import FileContents, FileEntry, Ignition
from utils.misc import octal_to_decimal, url_encode


def _nminterface(name: str, mtu: int) -> str:
    return url_encode(f"""[connection]
id={name}
type=ethernet
interface-name={name}

[ethernet]
mtu={mtu}
""")


def mtu9000_enable(ign: Ignition) -> None:
    """
    Adds MTU 9000 configuration files to the FILE_ENTRIES list.
    """

    ign['storage']['files'].extend([
        FileEntry(
            path="/etc/NetworkManager/system-connections/p0.nmconnection",
            overwrite=True,
            mode=octal_to_decimal(600),
            contents=FileContents(
                source=_nminterface("p0", 9216)
            )),
        FileEntry(
            path="/etc/NetworkManager/system-connections/p1.nmconnection",
            overwrite=True,
            mode=octal_to_decimal(600),
            contents=FileContents(
                source=_nminterface("p1", 9216)
            )
        ),
        FileEntry(
            path="/etc/NetworkManager/system-connections/pf0hpf.nmconnection",
            overwrite=True,
            mode=octal_to_decimal(600),
            contents=FileContents(
                source=_nminterface("pf0hpf", 9216)
            )
        ),
        FileEntry(
            path="/etc/NetworkManager/system-connections/pf1hpf.nmconnection",
            overwrite=True,
            mode=octal_to_decimal(600),
            contents=FileContents(
                source=_nminterface("pf1hpf", 9216)
            )
        )
    ])

    for file in ign['storage']['files']:
        if file['path'].endswith("/etc/NetworkManager/system-connections/pf0vf0.nmconnection"):
            if file['contents']["source"]:
                file['contents']["source"] = file['contents']["source"].replace(
                    "[ethernet]\n",
                    "[ethernet]\nmtu=9216\n"
                )
