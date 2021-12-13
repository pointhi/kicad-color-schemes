#!/usr/bin/env python3

import argparse
import pprint
from migrate_to_v6 import KEY_MAP as V6_KEY_MAP
import json
from pathlib import Path

pp = pprint.PrettyPrinter(indent=4)

V5_KEY_MAP = dict((tuple(v.split('.')), k) for (k, v) in V6_KEY_MAP.items())
FILEMAP = {
    "board": "pcbnew",
    "fpedit": "footprint_editor",
    "schematic": "eeschema"
}

def lookup_path(json_model, path):
    iter_step = json_model
    for key in path:
        if key in iter_step:
            iter_step = iter_step[key]
        else:
            return None
    return iter_step

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("json_config", type=Path,
        help="Kicad v6-style json color scheme")
    ap.add_argument("-o", "--output_dir",
        help="Ouput directory. Defaults to same folder as color scheme")
    args = ap.parse_args()
    base_dir = args.output_dir if args.output_dir else args.json_config.parent
    colormap = {}
    with open(args.json_config) as f:
        colorscheme = json.load(f)
        for (k, v) in V5_KEY_MAP.items():

            if k[0] not in colormap:
                colormap[k[0]] = {}
            color = lookup_path(colorscheme, k)
            if color: 
                colormap[k[0]][v] = color
    for (k, config) in FILEMAP.items():
        with open(base_dir / config, "w") as f:
            for (key, color) in colormap[k].items():
                f.write(f"{key}={color}\n")