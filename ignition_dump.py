#!/usr/bin/env python3

# adjusted from https://gist.github.com/sjenning/04dedeff2594c09ef1d8292e7b1eaae7

import json
import os
import sys
import base64
import gzip
import shutil
from urllib.parse import unquote


def dump_ignition(ign_path, out_root='ign-root'):
    if os.path.exists(out_root):
        while True:
            answer = input(f"Output directory '{out_root}' already exists. Overwrite? [y/n] ").strip().lower()
            if answer == 'y':
                break
            elif answer == 'n':
                print("Aborting.")
                return
        shutil.rmtree(out_root)

    ign_file = open(ign_path)
    ign_json = json.load(ign_file)
    ign_file.close()
    for file in ign_json['storage']['files']:
        path = file['path']
        if 'contents' in file:
            datatype, data = file['contents']['source'].split(',')
            os.makedirs(out_root + os.path.dirname(path), exist_ok=True)
            out_path = out_root + path
            out_file = open(out_path, "wb")
            compression = file.get('contents', {}).get('compression', '')
            try:
                if datatype == "data:text/plain" or datatype == 'data:':
                    raw = unquote(data).encode('utf-8')
                else:
                    raw = base64.b64decode(data)
                if compression == 'gzip':
                    raw = gzip.decompress(raw)
                out_file.write(raw)
            except:
                print(out_file, "failed", datatype)
            out_file.close()

            # Check if the dumped file is itself an ignition config
            try:
                nested = json.loads(raw)
                if 'ignition' in nested and 'storage' in nested:
                    while True:
                        answer = input(f"Inside the ignition {path} also looks like a nested ignition config. Dump it internally as well? [y/n] ").strip().lower()
                        if answer in ('y', 'n'):
                            break
                    if answer == 'y':
                        nested_root = os.path.join(os.path.dirname(out_path), 'ign-root')
                        dump_ignition(out_path, out_root=nested_root)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass


if __name__ == '__main__':
    dump_ignition(sys.argv[1])
