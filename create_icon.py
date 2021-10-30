#!/usr/bin/env python3

import argparse
import json
import re

from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent
ICON_EESCHEMA_SVG = ROOT_PATH / "icon_sch_base.svg"
ICON_PCBNEW_SVG = ROOT_PATH / "icon_pcb_base.svg"
METADATA_FILEAME = "metadata.json"

EESCHEMA_REPLACEMENT_TABLE = {
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

PCBNEW_REPLACEMENT_TABLE = {
    "#d0c5ac": "background",
    "#ff6600": "f_silks",
    "#ff00ff": "f_crtyd",
    "#000080": "f_fab",
    "#808000": "pad_through_hole",
    "#ff0000": "via_hole",
    "#ffff00": "via_through",
    "#00ff00": "copper_b",
    "#00ffff": "copper_f",
}


def parse_color(kicad_color):
    match = re.match(r"\s*rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", kicad_color)
    if match:
        red, green, blue = match.groups()
    else:
        match = re.match(r"\s*rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+.\d+)\s*\)", kicad_color)
        if not match:
            print(f"cannot parse color {kicad_color}")
            exit(1)
        red, green, blue, alpha = match.groups()
    return int(red), int(green), int(blue)


def replace_img(data, theme_json, replacement_table, theme_key):
    result_data = data
    for orig_color, replacement in replacement_table.items():
        if 'copper' in theme_json[theme_key]:
            # small hack
            theme_json[theme_key]['copper_f'] = theme_json[theme_key]['copper']['f']
            theme_json[theme_key]['copper_b'] = theme_json[theme_key]['copper']['b']

        replacement_str = theme_json[theme_key][replacement]
        red, green, blue = parse_color(replacement_str)
        replacement_color = f"#{red:02X}{green:02X}{blue:02X}"
        replace_regex = re.compile(re.escape(orig_color), re.IGNORECASE)
        result_data = replace_regex.sub(replacement_color, result_data)
    return result_data


def main():
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

    if 'schematic' in theme_json:
        print('create schematic icon')
        with ICON_EESCHEMA_SVG.open("r") as f:
            svg_data = f.read()

        svg_data = replace_img(svg_data, theme_json, EESCHEMA_REPLACEMENT_TABLE, 'schematic')

        icon_file = theme_dir / "icon_sch.svg"
        with icon_file.open("w") as f:
            f.write(svg_data)

    if 'board' in theme_json:
        print('create board icon')
        with ICON_PCBNEW_SVG.open("r") as f:
            svg_data = f.read()

        svg_data = replace_img(svg_data, theme_json, PCBNEW_REPLACEMENT_TABLE, 'board')

        icon_file = theme_dir / "icon_brd.svg"
        with icon_file.open("w") as f:
            f.write(svg_data)


if __name__ == "__main__":
    main()