#!/usr/bin/python3

import base64
import json
import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <ignition_file>", file=sys.stderr)
    sys.exit(1)

IGNITION_FILE = sys.argv[1]
BF_ENV = "/etc/bf.env"

# Read bf.env content once
with open(BF_ENV) as f:
    bf_env_content = f.read()

# Parse environment variables
env = {}
for line in bf_env_content.splitlines():
    line = line.strip()
    if line and '=' in line and not line.startswith('#'):
        key, value = line.split('=', 1)
        env[key] = value

# Load ignition file
with open(IGNITION_FILE) as f:
    ignition = json.load(f)

# Ensure storage.files exists
ignition.setdefault('storage', {}).setdefault('files', [])

ignition['storage']['files'].append({
    'path': '/etc/bf.env',
    'overwrite': True,
    'mode': 420,
    'contents': {
        'source': 'data:text/plain;charset=utf-8;base64,' + base64.b64encode(bf_env_content.encode()).decode()
    }
})

if 'HOSTNAME' in env:
    ignition['storage']['files'].append({
        'path': '/etc/hostname',
        'overwrite': True,
        'mode': 420,
        'contents': {
            'source': 'data:,' + env['HOSTNAME']
        }
    })
else:
    print("Warning: HOSTNAME not found in bf.env, skipping /etc/hostname", file=sys.stderr)

with open(IGNITION_FILE, 'w') as f:
    json.dump(ignition, f, indent=4)
