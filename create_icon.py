#!/usr/bin/env python3

import argparse
import json
import re

from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent
ICON_EESCHEMA_SVG = ROOT_PATH / "icon_sch_base.svg"
METADATA_FILEAME = "metadata.json"

REPLACEMENT_TABLE = {
    "#d0c5ac": "background",
    "#00ff00": "wire",
    "#999999": "component_body",
    "#ff0000": "component_outline",
    "#0000ff": "pin",
    "#ff6600": "pin_name",
    "#ffff00": "pin_number",
    "#000080": "reference",
    "#800080": "value"
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create SVG icon applied by color scheme')
    parser.add_argument('theme_dir', type=str)

    args = parser.parse_args()

    theme_dir = Path(args.theme_dir)
    if not theme_dir.is_dir():
        print(f"{theme_dir} is not a directory")
        exit(1)

    for theme_file in theme_dir.glob("*.json"):
        if theme_file.name != METADATA_FILEAME:
            with theme_file.open("r") as f:
                print(f"found {theme_file}")
                theme_json = json.load(f)
                break
    else:
        print(f"no .json found in {theme_dir}")
        exit(1)

    with ICON_EESCHEMA_SVG.open("r") as f:
        svg_data = f.read()

    for orig_color, replacement in REPLACEMENT_TABLE.items():
        replacement_str = theme_json['schematic'][replacement]
        match = re.match(r"\s*rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", replacement_str)
        if not match:
            print(f"cannot find color for {replacement} in theme!")
            exit(1)
        red, green, blue = match.groups()
        replacement_color = f"#{int(red):02X}{int(green):02X}{int(blue):02X}"
        print(f"{replacement} = {replacement_color}")
        replace_regex = re.compile(re.escape(orig_color), re.IGNORECASE)
        svg_data = replace_regex.sub(replacement_color, svg_data)

        #svg_data = svg_data.replace(orig_color, replacement_color)

    icon_file = theme_dir / "icon.svg"
    with icon_file.open("w") as f:
        f.write(svg_data)
