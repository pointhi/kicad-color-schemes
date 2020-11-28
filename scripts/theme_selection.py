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
    print('        Command: python3 scripts/patch.py <themes/selected-theme/> <path/to/your/eeschema/folder/>')
    print('        IMPORTANT NOTE: You may need to back up your eeschema and pcbnew files manually first.\n')
    sys.exit(1)

def get_user_preferences_path():
    """
    Retrieve the eeschema and pcbnew folder path based on the operating system.

    Arguments:
        None

    Returns:
        Path -- This is the ABSOLUTE path to preference folder.
    """
    preferences_path = ''

    if sys.platform == 'linux':
        preferences_path = os.path.join(os.getenv('HOME'), '.config/kicad')
    elif sys.platform == 'darwin':
        preferences_path = os.path.join(os.getenv('HOME'), 'Library/Preferences/kicad')
    elif sys.platform == 'win32':
        preferences_path = os.path.join('c:\\', 'Users', os.getlogin(), 'AppData', 'Roaming', 'kicad')
    else:
        error('Unsupported OS detected.')

    return preferences_path

def backup():
    """
    First checks for the presence of the backup directory. If it is not present, this function
    will create it and copy the original eeschema & pcbnew files to it based on the operating 
    system. The following operating systems are supported:
      - Linux Distributions
      - MacOS
      - Windows

    Arguments:
        None

    Returns:
        None
    """
    # The backups should be stored in the user preference folder
    preferences_folder = get_user_preferences_path()

    # If the eeschema backup isn't present, then backups have not yet been made
    backup_eeschema = os.path.join(preferences_folder, 'eeschema.bak')
    if not os.path.exists(backup_eeschema):
        # Find the original eeschema and make sure it exists where it should
        original_eeschema = os.path.join(preferences_folder, 'eeschema')
        if not os.path.exists(original_eeschema):
            error('Unable to find {}'.format(original_eeschema))

        # Find the original pcbnew and make sure it exists where it should
        original_pcbnew = os.path.join(preferences_folder, 'pcbnew')
        if not os.path.exists(original_pcbnew):
            error('Unable to find {}'.format(original_pcbnew))

        # Copy the original eeschema into the backup directory
        backup_eeschema_path = os.path.join(preferences_folder,'eeschema.bak')
        print('\n[Info] Backing up {} to {}'.format(original_eeschema, backup_eeschema_path))
        try:
            shutil.copyfile(original_eeschema, backup_eeschema_path)
        except:
            error('Unable to copy {} to {}'.format(original_eeschema, preferences_folder))

        # Copy the original pcbnew into the backup directory
        backup_pcbnew_path = os.path.join(preferences_folder,'pcbnew.bak')
        print('[Info] Backing up {} to {}'.format(original_pcbnew, backup_pcbnew_path))
        try:
            shutil.copyfile(original_pcbnew, backup_pcbnew_path)
        except:
            # Remove the eeschema backup so it doesn't signify good backup on next run
            os.remove(os.path.join(preferences_folder,'eeschema.bak'))
            error('Unable to copy {} to {}'.format(original_pcbnew, preferences_folder))
    else:
        print('\n[Info] Backup files are 1already present in {}'.format(preferences_folder))

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

def install_theme(theme_dir, theme):
    """
    Installs the specified theme  

    Arguments:
        theme_dir {Path} -- Path location of theme directory relative to top-level Makefile.
        themes {string} -- Available theme options.

    Returns:
        None 
    """ 
    # Define the preferences folder to reduce function calls
    preferences_folder = get_user_preferences_path()
    
    # If backup restoration is selected, overwrite the existing eeschema and pcbnew
    # files with the eeschema.bak and pcbnew.bak backup files. 
    if theme == 'restore_backup':
        print("[Info] Restoring Backup")
        # Copy the backup files over the existing preference files
        shutil.copyfile(os.path.join(preferences_folder,'eeschema.bak'),
            os.path.join(preferences_folder, 'eeschema'))
        shutil.copyfile(os.path.join(preferences_folder,'pcbnew.bak'),
            os.path.join(preferences_folder, 'pcbnew'))
    
    # Otherwise, call patch.py to install the selected theme
    else:
        theme_config_folder = os.path.join(os.getcwd(), theme_dir, theme)
        print("[Info] Installing Theme: {}".format(theme))
        print('[Info] SRC:  {}/eeschema'.format(theme_config_folder))
        print('[Info] DEST: {}/eeschema\n'.format(preferences_folder))     
        # Call patch.py to install the selected theme
        os.system('python3 scripts/patch.py {} {}'.format(theme_config_folder, preferences_folder))

def main():
    # Add & Parse available arguments
    parser = argparse.ArgumentParser(description='Display and select KiCAD theme to be installed')
    parser.add_argument('theme_dir', type=Path, nargs=1, help='Theme dir for KiCAD themes')
    args = parser.parse_args()

    # First and foremost, backup the existing eeschema if not done already
    backup()

    # Find & select theme
    theme = select_theme(args.theme_dir[0])

    # Use patch.py to install the selected theme
    install_theme(args.theme_dir[0], theme)

if __name__ == '__main__':
    main()