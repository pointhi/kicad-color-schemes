#!/usr/bin/env python3
import sys, os
import argparse
from collections import OrderedDict
from pathlib import Path
import shutil

class ConfigFile():
    def __init__(self, filepath):
        self.content = OrderedDict()
        self.filepath = filepath
        with open(filepath, 'r') as file:
            idx = 0
            for line in file:
                l = line.strip()
                #print(line.startswith('#'), line)
                if l != '' and not (line.startswith('[') or line.startswith('#')):
                    try:
                        key, value = l.split('=', 1)
                    except:
                        raise ValueError("line {}: '{}' is of invalid format in config file.".format(idx, l))
                    self.content.update({key: value})
                    idx += 1

    def patch(self, patchfile):
        with open(patchfile, 'r') as file:
            idx = 0
            for line in file:
                l = line.strip()
                if l == '' or (line.startswith('[') or line.startswith('#')):
                    continue

                try:
                    key, value = l.split('=')
                except:
                    raise ValueError("line {}: '{}' is of invalid format in patch file.".format(idx, l))

                self.content[key] = value
                idx += 1

    def write(self):
        with open(self.filepath, 'w') as file:
            for key, value in self.content.items():
                print("{}={}".format(key, value), file=file)

parser = argparse.ArgumentParser(description='Patch the KiCad settings file with the given colour scheme.')
parser.add_argument('scheme_path', type=Path, nargs=1,
                        help='Path to scheme definition.')
parser.add_argument('config_dir', type=Path, nargs=1,
                        help='Path to kicad config directory')
parser.add_argument('-p', '--pcb_disable', action='store_true', help='Disable patching of pcb_new colour definition')
parser.add_argument('-f', '--footprint_disable', action='store_true', help='Disable patching of footprint editor colour definition')
parser.add_argument('-e', '--eeschema_disable', action='store_true', help='Disable patching of eeschema and symbol editor colour definition')

args = parser.parse_args()


if args.pcb_disable and args.footprint_disable and args.eeschema_disable:
    print("All definitions disabled. Nothing to do. (Use --help for instructions.)")
    exit()

if not args.config_dir[0].is_dir():
    print("'{}' expected to be the kicad config directory but it is not a directory or does not exist. (Use --help for instructions.)".format(args.config_dir[0]))
    exit()

if not args.scheme_path[0].is_dir():
    print("'{}' expected to be the colour scheme definition directory but it is not a directory or does not exist. (Use --help for instructions.)".format(args.scheme_path[0]))

if not args.eeschema_disable:
    ee_patch = args.scheme_path[0] / 'eeschema'
    if not ee_patch.is_file():
        print("Scheme does not contain a definition for EESchema, skipped.")
    else:
        print("Updating EESchema configuration.")
        ee_config = args.config_dir[0] / 'eeschema'
        try:
            shutil.copy(ee_config, str(ee_config)+".bak")
        except:
            answer = input("Unable to create backup file. Continue anyways? [y/n] ")
            while(answer not in ['y', 'n']):
                answer = input("Unable to create backup file. Continue anyways? [y/n] ")
            if answer == 'n':
                exit()


        eeschema_handler = ConfigFile(ee_config)
        eeschema_handler.patch(ee_patch)
        eeschema_handler.write()

if args.pcb_disable and args.footprint_disable:
    print("Done")
    exit()

pcb_config = args.config_dir[0] / 'pcbnew'
try:
    shutil.copy(pcb_config, str(pcb_config)+".bak")
except:
    answer = input("Unable to create backup file. Continue anyways? [y/n] ")
    while(answer not in ['y', 'n']):
        answer = input("Unable to create backup file. Continue anyways? [y/n] ")
    if answer == 'n':
        exit()

pcb_handler = ConfigFile(pcb_config)

if not args.pcb_disable:
    pcb_patch = args.scheme_path[0] / 'pcbnew'
    if not pcb_patch.is_file():
        print("Scheme does not contain a definition for pcb_new, skipped.")
    else:
        print("Updating pcb_new configuration.")
        pcb_handler.patch(pcb_patch)

if not args.footprint_disable:
    fpe_patch = args.scheme_path[0] / 'footprint_editor'
    if not fpe_patch.is_file():
        print("Scheme does not contain a definition for the footprint editor, skipped.")
    else:
        print("Updating footprint editor configuration.")
        pcb_handler.patch(fpe_patch)

pcb_handler.write()
