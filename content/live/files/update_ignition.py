#!/usr/bin/python3

import json
import configparser

BF_ENV = "/etc/bf.env"
IGNITION_FILE = "/var/lib/hcp/hcp.ign"

env = configparser.ConfigParser()
env.read(BF_ENV)

env.get('HOSTNAME')
env.get('KERNEL_PARAMETERS')
env.get('NVCONFIG_PARAMS')
env.get('DPF_SF_NUM')
env.get('DPF_TRUSTED_SFS')

ignition = json.load(open(IGNITION_FILE))

ignition['storage']['files'].append({
    'path': '/etc/bf.env',
    'overwrite': True,
    'mode': 644,
    'contents': {
        'source': 'data:,' + open(BF_ENV).read()
    }
})

# /etc/hostname
ignition['storage']['files'].append({
    'path': '/etc/hostname',
    'overwrite': True,
    'mode': 644,
    'contents': {
        'inline': env.get('HOSTNAME')
    }
})

with open(IGNITION_FILE, 'w') as f:
    json.dump(ignition, f, indent=4)
