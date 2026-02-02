#!/usr/bin/python3

import base64
import json

BF_ENV = "/etc/bf.env"
IGNITION_FILE = "/var/lib/hcp/hcp.ign"

env = {}
with open(BF_ENV) as f:
    for line in f:
        line = line.strip()
        if line and '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            env[key] = value

ignition = json.load(open(IGNITION_FILE))

ignition['storage']['files'].append({
    'path': '/etc/bf.env',
    'overwrite': True,
    'mode': 420,
    'contents': {
        'source': 'data:text/plain;charset=utf-8;base64,' + base64.b64encode(open(BF_ENV).read().encode()).decode()
    }
})

ignition['storage']['files'].append({
    'path': '/etc/hostname',
    'overwrite': True,
    'mode': 420,
    'contents': {
        'source': 'data:,' + env['HOSTNAME']
    }
})

with open(IGNITION_FILE, 'w') as f:
    json.dump(ignition, f, indent=4)
