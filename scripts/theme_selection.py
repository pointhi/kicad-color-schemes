#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

def error(err_msg):
    """
    Prints

    Arguments:
        err_msg {string} -- Error message to be displayed

    Returns:
        None
    """
    print('[Error] {}\n'.format(err_msg))
    print('        Run patch.py and manually point to your desired theme and eeschema location')
    print('        IMPORTANT NOTE: You will need to back up your eeschema file manually FIRST\n')
    sys.exit(1)

def get_eeschema_path():
    """
    Retrieve the eeschema path based on the operating system.

    Arguments:
        None

    Returns:
        Path -- This is the ABSOLUTE path to eeschema file.
    """
    eeschema_path = ''

    if sys.platform == 'linux':
        eeschema_path = os.path.join(os.getenv('HOME'), '.config/kicad')
    elif sys.platform == 'darwin':
        eeschema_path = os.path.join(os.getenv('HOME'), 'Library/Preferences/kicad')
    elif sys.platform == 'win32':
        # eeschema_path = os.path.join('c:/', 'Users', os.getlogin(), 'AppData', 'Roaming', 'kicad')
        eeschema_path = os.path.join('c:/', 'Program Files', 'KiCAD', 'bin')
    else:
        error('Unsupported OS detected.')

    return eeschema_path

def backup(backup_dir):
    """
    First checks for the presence of the backup directory. If it is not present, this function
    will create it and copy the original eeschema file to it based on the operating system. The
    following operating systems are supported:
      - Linux Distributions
      - MacOS
      - Windows

    Arguments:
        backup_dir {Path} -- Path location of backup directory relative to top-level Makefile.

    Returns:
        None
    """
    if not os.path.exists(backup_dir):
        # Find the original eeschema and make sure it exists where it should
        original_eeschema = os.path.join(get_eeschema_path(), 'eeschema')
        if not os.path.exists(original_eeschema):
            error('Unable to find {}'.format(original_eeschema))

        # Make the backup directory
        print('[Info] Making backup directory {}/'.format(backup_dir))
        os.mkdir(backup_dir)

        # Copy the original eeschema into the backup directory
        print('[Info] Backing up {} to {}/'.format(original_eeschema, backup_dir))
        try:
            shutil.copyfile(original_eeschema, os.path.join(backup_dir,'eeschema'))
        except:
            os.rmdir(backup_dir)
            error('Unable to copy {} to {}'.format(original_eeschema, backup_dir))
    else:
        print('[Info] Backup eeschema already present in {}'.format(backup_dir))

def find_themes(theme_dir):
    """
    Finds available themes from the theme directory and populate a list of available options. 

    Arguments:
        theme_dir {Path} - Path location of theme directory relative to top-level Makefile.

    Returns:
        string list -- Theme names of the available theme options.
    """
    # Create an empty list for themes
    themes = []

    with os.scandir(theme_dir) as dir:
        for entry in dir:
            if entry.is_dir():
                themes.append(entry.name)

    # Organize the themes alphabetically and then add restore backup as the first in the list
    themes = sorted(themes)
    themes = ['restore_backup'] + themes

    return themes

def select_theme(theme_dir):
    """
    Prompts user to select a theme option from the available choices.  

    Arguments:
        theme_dir {Path} - Path location of theme directory relative to top-level Makefile.

    Returns:
        string -- The selected theme. 
    """
    # First, find available themes
    themes = find_themes(theme_dir)

    while True:
        # Display the themes for the user to select and prompt for a selection
        print('\n')
        for index,theme in enumerate(themes):
            if index < 9:
                print('{}.  {}'.format(index + 1, theme))
            else:
                print('{}. {}'.format(index + 1, theme))
        selection = input('\nSelect a Number: ')

        if selection.isnumeric():
            selection = int(selection)

            if selection <= len(themes):
                return themes[selection-1]

def install_theme(backup_dir, theme_dir, theme):
    """
    Installs the specified theme  

    Arguments:
        backup_dir {Path} -- Path location of backup directory relative to top-level Makefile.
        theme_dir {Path} -- Path location of theme directory relative to top-level Makefile.
        themes {string} -- Available theme options.

    Returns:
        None 
    """ 
    # If backup restorating is selected, simply copy back the original eeschema
    if theme == 'restore_backup':
        print("[Info] Restoring Backup")
        original_eeschema = os.path.join(os.getcwd(), backup_dir, 'eeschema')
        shutil.copyfile(original_eeschema, os.path.join(get_eeschema_path(), 'eeschema'))
    # Otherwise, call patch.py to install the selected theme
    else:
        theme_config_path = os.path.join(os.getcwd(), theme_dir, theme)
        print("[Info] Installing Theme: {}".format(theme))
        print('[Info] SRC:  {}/eeschema'.format(theme_config_path))
        print('[Info] DEST: {}/eeschema\n'.format(str(get_eeschema_path())))
        os.system('python3 scripts/patch.py {} {}'.format( \
            str(theme_config_path), str(get_eeschema_path())))

def main():
    # Add & Parse available arguments
    parser = argparse.ArgumentParser(description='Display and select KiCAD theme to be installed')
    parser.add_argument('backup_dir', type=Path, nargs=1, help='Backup dir for original eeschema')
    parser.add_argument('theme_dir', type=Path, nargs=1, help='Theme dir for KiCAD themes')
    args = parser.parse_args()

    # First and foremost, backup the existing eeschema if not done already
    backup(args.backup_dir[0])

    # Find & select theme
    theme = select_theme(args.theme_dir[0])

    # Use patch.py to install the selected theme
    install_theme(args.backup_dir[0], args.theme_dir[0], theme)

if __name__ == '__main__':
    main()