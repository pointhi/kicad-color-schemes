#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import re


KEY_MAP = {
    "Color4DBgCanvasEx":            "schematic.background",
    "Color4DBodyBgEx":              "schematic.component_body",
    "Color4DBodyEx":                "schematic.component_outline",
    "Color4DBrightenedEx":          "schematic.brightened",
    "Color4DBrighenedEx":           "schematic.brightened",
    "Color4DBusEx":                 "schematic.bus",
    "Color4DConnEx":                "schematic.junction",
    "Color4DCursorEx":              "schematic.cursor",
    "Color4DErcEEx":                "schematic.erc_error",
    "Color4DErcWEx":                "schematic.erc_warning",
    "Color4DFieldEx":               "schematic.fields",
    "Color4DGLabelEx":              "schematic.label_global",
    "Color4DGridEx":                "schematic.grid",
    "Color4DHLabelEx":              "schematic.label_hier",
    "Color4DHiddenEx":              "schematic.hidden",
    "Color4DLLabelEx":              "schematic.label_local",
    "Color4DNetNameEx":             "schematic.net_name",
    "Color4DNoConnectEx":           "schematic.no_connect",
    "Color4DNoteEx":                "schematic.note",
    "Color4DPinEx":                 "schematic.pin",
    "Color4DPinNameEx":             "schematic.pin_name",
    "Color4DPinNumEx":              "schematic.pin_number",
    "Color4DReferenceEx":           "schematic.reference",
    "Color4DShadowEx":              "schematic.shadow",
    "Color4DSheetEx":               "schematic.sheet",
    "Color4DSheetFileNameEx":       "schematic.sheet_filename",
    "Color4DSheetLabelEx":          "schematic.sheet_label",
    "Color4DSheetNameEx":           "schematic.sheet_name",
    "Color4DValueEx":               "schematic.value",
    "Color4DWireEx":                "schematic.wire",
    "Color4DWorksheetEx":           "schematic.worksheet",

    "Color4DAnchorEx":              "board.anchor",
    "Color4DAuxItems":              "board.aux_items",
    "Color4DPCBBackground":         "board.background",
    "Color4DPCBCursor":             "board.cursor",
    "Color4DTxtBackEx":             "board.footprint_text_back",
    "Color4DTxtFrontEx":            "board.footprint_text_front",
    "Color4DTxtInvisEx":            "board.footprint_text_invisible",
    "Color4DGrid":                  "board.grid",
    "Color4DNoNetPadMarker":        "board.no_connect",
    "Color4DPadBackEx":             "board.pad_back",
    "Color4DPadFrontEx":            "board.pad_front",
    "Color4DNonPlatedEx":           "board.plated_hole",
    "Color4DPadThruHoleEx":         "board.pad_through_hole",
    "Color4DRatsEx":                "board.ratsnest",
    "Color4DViaBBlindEx":           "board.via_blind_buried",
    "Color4DViaMicroEx":            "board.via_micro",
    "Color4DViaThruEx":             "board.via_through",
    "Color4DWorksheet":             "board.worksheet",
    "Color4DPCBLayer_F.Cu":         "board.copper.f",
    "Color4DPCBLayer_In1.Cu":       "board.copper.in1",
    "Color4DPCBLayer_In2.Cu":       "board.copper.in2",
    "Color4DPCBLayer_In3.Cu":       "board.copper.in3",
    "Color4DPCBLayer_In4.Cu":       "board.copper.in4",
    "Color4DPCBLayer_In5.Cu":       "board.copper.in5",
    "Color4DPCBLayer_In6.Cu":       "board.copper.in6",
    "Color4DPCBLayer_In7.Cu":       "board.copper.in7",
    "Color4DPCBLayer_In8.Cu":       "board.copper.in8",
    "Color4DPCBLayer_In9.Cu":       "board.copper.in9",
    "Color4DPCBLayer_In10.Cu":      "board.copper.in10",
    "Color4DPCBLayer_In11.Cu":      "board.copper.in11",
    "Color4DPCBLayer_In12.Cu":      "board.copper.in12",
    "Color4DPCBLayer_In13.Cu":      "board.copper.in13",
    "Color4DPCBLayer_In14.Cu":      "board.copper.in14",
    "Color4DPCBLayer_In15.Cu":      "board.copper.in15",
    "Color4DPCBLayer_In16.Cu":      "board.copper.in16",
    "Color4DPCBLayer_In17.Cu":      "board.copper.in17",
    "Color4DPCBLayer_In18.Cu":      "board.copper.in18",
    "Color4DPCBLayer_In19.Cu":      "board.copper.in19",
    "Color4DPCBLayer_In20.Cu":      "board.copper.in20",
    "Color4DPCBLayer_In21.Cu":      "board.copper.in21",
    "Color4DPCBLayer_In22.Cu":      "board.copper.in22",
    "Color4DPCBLayer_In23.Cu":      "board.copper.in23",
    "Color4DPCBLayer_In24.Cu":      "board.copper.in24",
    "Color4DPCBLayer_In25.Cu":      "board.copper.in25",
    "Color4DPCBLayer_In26.Cu":      "board.copper.in26",
    "Color4DPCBLayer_In27.Cu":      "board.copper.in27",
    "Color4DPCBLayer_In28.Cu":      "board.copper.in28",
    "Color4DPCBLayer_In29.Cu":      "board.copper.in29",
    "Color4DPCBLayer_In30.Cu":      "board.copper.in30",
    "Color4DPCBLayer_B.Cu":         "board.copper.b",
    "Color4DPCBLayer_B.Adhes":      "board.b_adhes",
    "Color4DPCBLayer_F.Adhes":      "board.f_adhes",
    "Color4DPCBLayer_B.Paste":      "board.b_paste",
    "Color4DPCBLayer_F.Paste":      "board.f_paste",
    "Color4DPCBLayer_B.SilkS":      "board.b_silks",
    "Color4DPCBLayer_F.SilkS":      "board.f_silks",
    "Color4DPCBLayer_B.Mask":       "board.b_mask",
    "Color4DPCBLayer_F.Mask":       "board.f_mask",
    "Color4DPCBLayer_Dwgs.User":    "board.dwgs_user",
    "Color4DPCBLayer_Cmts.User":    "board.cmts_user",
    "Color4DPCBLayer_Eco1.User":    "board.eco1_user",
    "Color4DPCBLayer_Eco2.User":    "board.eco2_user",
    "Color4DPCBLayer_Edge.Cuts":    "board.edge_cuts",
    "Color4DPCBLayer_Margin=rgb":   "board.margin",
    "Color4DPCBLayer_B.CrtYd":      "board.b_crtyd",
    "Color4DPCBLayer_F.CrtYd":      "board.f_crtyd",
    "Color4DPCBLayer_B.Fab":        "board.b_fab",
    "Color4DPCBLayer_F.Fab":        "board.f_fab",

    "ModEditColor4DAnchorEx":              "fpedit.anchor",
    "ModEditColor4DAuxItems":              "fpedit.aux_items",
    "ModEditColor4DPCBBackground":         "fpedit.background",
    "ModEditColor4DPCBCursor":             "fpedit.cursor",
    "ModEditColor4DTxtBackEx":             "fpedit.footprint_text_back",
    "ModEditColor4DTxtFrontEx":            "fpedit.footprint_text_front",
    "ModEditColor4DTxtInvisEx":            "fpedit.footprint_text_invisible",
    "ModEditColor4DGrid":                  "fpedit.grid",
    "ModEditColor4DPadBackEx":             "fpedit.pad_back",
    "ModEditColor4DPadFrontEx":            "fpedit.pad_front",
    "ModEditColor4DNonPlatedEx":           "fpedit.plated_hole",
    "ModEditColor4DPadThruHoleEx":         "fpedit.pad_through_hole",
    "ModEditColor4DWorksheet":             "fpedit.worksheet",
    "ModEditColor4DPCBLayer_F.Cu":         "fpedit.copper.f",
    "ModEditColor4DPCBLayer_In1.Cu":       "fpedit.copper.in1",
    "ModEditColor4DPCBLayer_In2.Cu":       "fpedit.copper.in2",
    "ModEditColor4DPCBLayer_In3.Cu":       "fpedit.copper.in3",
    "ModEditColor4DPCBLayer_In4.Cu":       "fpedit.copper.in4",
    "ModEditColor4DPCBLayer_In5.Cu":       "fpedit.copper.in5",
    "ModEditColor4DPCBLayer_In6.Cu":       "fpedit.copper.in6",
    "ModEditColor4DPCBLayer_In7.Cu":       "fpedit.copper.in7",
    "ModEditColor4DPCBLayer_In8.Cu":       "fpedit.copper.in8",
    "ModEditColor4DPCBLayer_In9.Cu":       "fpedit.copper.in9",
    "ModEditColor4DPCBLayer_In10.Cu":      "fpedit.copper.in10",
    "ModEditColor4DPCBLayer_In11.Cu":      "fpedit.copper.in11",
    "ModEditColor4DPCBLayer_In12.Cu":      "fpedit.copper.in12",
    "ModEditColor4DPCBLayer_In13.Cu":      "fpedit.copper.in13",
    "ModEditColor4DPCBLayer_In14.Cu":      "fpedit.copper.in14",
    "ModEditColor4DPCBLayer_In15.Cu":      "fpedit.copper.in15",
    "ModEditColor4DPCBLayer_In16.Cu":      "fpedit.copper.in16",
    "ModEditColor4DPCBLayer_In17.Cu":      "fpedit.copper.in17",
    "ModEditColor4DPCBLayer_In18.Cu":      "fpedit.copper.in18",
    "ModEditColor4DPCBLayer_In19.Cu":      "fpedit.copper.in19",
    "ModEditColor4DPCBLayer_In20.Cu":      "fpedit.copper.in20",
    "ModEditColor4DPCBLayer_In21.Cu":      "fpedit.copper.in21",
    "ModEditColor4DPCBLayer_In22.Cu":      "fpedit.copper.in22",
    "ModEditColor4DPCBLayer_In23.Cu":      "fpedit.copper.in23",
    "ModEditColor4DPCBLayer_In24.Cu":      "fpedit.copper.in24",
    "ModEditColor4DPCBLayer_In25.Cu":      "fpedit.copper.in25",
    "ModEditColor4DPCBLayer_In26.Cu":      "fpedit.copper.in26",
    "ModEditColor4DPCBLayer_In27.Cu":      "fpedit.copper.in27",
    "ModEditColor4DPCBLayer_In28.Cu":      "fpedit.copper.in28",
    "ModEditColor4DPCBLayer_In29.Cu":      "fpedit.copper.in29",
    "ModEditColor4DPCBLayer_In30.Cu":      "fpedit.copper.in30",
    "ModEditColor4DPCBLayer_B.Cu":         "fpedit.copper.b",
    "ModEditColor4DPCBLayer_B.Adhes":      "fpedit.b_adhes",
    "ModEditColor4DPCBLayer_F.Adhes":      "fpedit.f_adhes",
    "ModEditColor4DPCBLayer_B.Paste":      "fpedit.b_paste",
    "ModEditColor4DPCBLayer_F.Paste":      "fpedit.f_paste",
    "ModEditColor4DPCBLayer_B.SilkS":      "fpedit.b_silks",
    "ModEditColor4DPCBLayer_F.SilkS":      "fpedit.f_silks",
    "ModEditColor4DPCBLayer_B.Mask":       "fpedit.b_mask",
    "ModEditColor4DPCBLayer_F.Mask":       "fpedit.f_mask",
    "ModEditColor4DPCBLayer_Dwgs.User":    "fpedit.dwgs_user",
    "ModEditColor4DPCBLayer_Cmts.User":    "fpedit.cmts_user",
    "ModEditColor4DPCBLayer_Eco1.User":    "fpedit.eco1_user",
    "ModEditColor4DPCBLayer_Eco2.User":    "fpedit.eco2_user",
    "ModEditColor4DPCBLayer_Edge.Cuts":    "fpedit.edge_cuts",
    "ModEditColor4DPCBLayer_Margin=rgb":   "fpedit.margin",
    "ModEditColor4DPCBLayer_B.CrtYd":      "fpedit.b_crtyd",
    "ModEditColor4DPCBLayer_F.CrtYd":      "fpedit.f_crtyd",
    "ModEditColor4DPCBLayer_B.Fab":        "fpedit.b_fab",
    "ModEditColor4DPCBLayer_F.Fab":        "fpedit.f_fab",
}


def recursive_insert(dictionary, keys, value):
    if len(keys) > 1:
        key = keys.pop(0)
        if key in dictionary:
            nested = dictionary[key]
        else:
            nested = dict()
        dictionary[key] = recursive_insert(nested, keys, value)
        return dictionary
    else:
        dictionary[keys[0]] = value
        return dictionary


def main():
    parser = argparse.ArgumentParser(description='Migrate a scheme to V6 JSON format')
    parser.add_argument('scheme_path', type=Path, nargs=1, help='Path to scheme definition')
    parser.add_argument('name', type=str, nargs=1, help='Display name of the output theme')

    args = parser.parse_args()

    if not args.scheme_path[0].is_dir():
        print("'{}' needs to be the directory of a scheme".format(args.scheme_path[0]))

    filename = args.scheme_path[0].stem

    json_data = {
        "meta": {
            "filename": filename,
            "version": 0,
            "name": args.name[0]
        }
    }

    for file in ['eeschema', 'pcbnew', 'footprint_editor']:
        fp  = args.scheme_path[0] / file

        if not fp.is_file():
            continue

        print("Migrating {}".format(fp.name))

        data = {}

        with open(fp, 'r') as f:
            for line in f:
                l = line.strip()

                if l == '':
                    continue

                try:
                    key, color = l.split('=')
                except:
                    continue

                if color is not None:
                    try:
                        json_key = KEY_MAP[key]
                    except:
                        print("Warning: unknown key {}".format(key))
                        continue

                    keys = json_key.split('.')

                    if file == 'footprint_editor':
                        keys[0] = 'fpedit'

                    recursive_insert(data, keys, color)

        json_data.update(data)


    new_file_path = args.scheme_path[0] / (filename + ".json")
    with open(new_file_path, 'w') as f:
        json.dump(json_data, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
