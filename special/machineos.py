import json
import urllib
from utils.datatypes import Ignition


def replace_machine_os_url(ign: Ignition, machine_os_url: str):
    """
    Preprocesses the ignition file to disable the machine-config-daemon-firstboot.service
    and enable the openvswitch.service.
    """

    for s in ign['storage']['files']:
        if s['path'] == '/etc/ignition-machine-config-encapsulated.json':
            print(f"Replacing machine OS URL")

            decoded_text = urllib.parse.unquote(
                s['contents']['source'].split('data:,')[1])
            decoded_json = json.loads(decoded_text)

            decoded_json['spec']['osImageURL'] = machine_os_url

            encoded_text = urllib.parse.quote(json.dumps(decoded_json))
            s['contents']['source'] = f"data:,{encoded_text}"
            return
    raise Exception("Machine OS URL not found")
