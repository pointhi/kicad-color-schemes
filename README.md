# kicad-color-schemes

Want to change the color scheme of KiCad? Look here for inspiration.

## How to use a colour theme.

Every theme directory contains the colour definition parts of the eeschema and pcbnew setup files found in your personal profile.
- For Linux under ~.config/kicad/
- Windows XP: “C:\Documents and Settings\username\Application Data” + kicad (= %APPDATA%\kicad)
- Windows Vista & later: “C:\Users\username\AppData\Roaming” + kicad (= %APPDATA%\kicad)
- OSX: The user’s home directory + /Library/Preferences/kicad

Use a text editor to overwrite the relevant sections with the data found in the files in this folder. **Make sure you create a backup first.**

The pcbnew config file content has been split into the sections responsible for the footprint editor and the one for pcbnew. This is done to allow you to more easily mix and match different schemes for different tools.

## Automatic patcher

An automatic patch script can be used to transfer a colour scheme into your KiCad settings files. Make sure KiCad is closed before using it.

The script expects the directory containing the colour scheme and the kicad config directory as arguments. Switches are included to disable transfer of a particular part of the scheme definition. (use --help for detailed instructions.) A bakup of your settings files is created before changes are made.

Example:
`python3 patch.py ~/kicad-color-schemes/blue-green-dark/ ~/.config/kicad/`

## JSON themes (for KiCad 6, and "5.99" nightly builds after February 2020)

KiCad 6 is changing to a JSON-based colour theme system.  Recent nightly builds already support the
new system, where each colour theme lives in a JSON file in the `colors` directory of the user
settings path (see "How to use a colour theme" above.)

To use the JSON version of a theme, just copy the file into your `colors` directory.  The next time
you run KiCad, it will detect the new theme file and you will be able to choose it in the
preferences.  Each KiCad application can use a different color theme if you wish.

In the new system, the footprint editor and PcbNew use the same color theme.  If you would like to
have different colours for those two applications, the way to do it is to choose a different theme
file in the PcbNew and footprint editor preferences dialogs.

## eeschema

color-scheme                                               | screenshot
-----------------------------------------------------------|-----------
**kicad-default**                                          | ![Default theme by KiCad](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-default/eeschema.png)
**solarized-dark** *http://ethanschoonover.com/solarized*  | ![Dark theme based on solarized](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/solarized-dark/eeschema.png)
**solarized-light** *http://ethanschoonover.com/solarized* | ![Light theme based on solarized](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/solarized-light/eeschema.png)
**sw**                                                     | ![simple black/white theme](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/sw/eeschema.png)
**blue-tone**     | ![Blue tone theme](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/blue-tone/eeschema.png)
**behave-dark** *https://atom.io/themes/behave-theme*      | ![Dark theme based on behave](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/behave-dark/eeschema.png)
**neon** *Inspired by forum user BobZ*      | ![Neon coloured theme inspired by forum user BobZ](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/neon/eeschema.png)

## pcbnew
color-scheme                                               | screenshot
-----------------------------------------------------------|-----------
**kicad-default**                                          | ![Default theme by KiCad](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-default/pcbnew.png)
**behave-dark** *https://atom.io/themes/behave-theme*      | ![Dark theme based on behave](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/behave-dark/pcbnew.png)
**blue-green-dark**     | ![Dark theme using blue and green](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/blue-green-dark/pcbnew.png)

## footprint editor
color-scheme                                               | screenshot
-----------------------------------------------------------|-----------
**kicad-default**                                          | ![Default theme by KiCad](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-default/footprint_editor.png)
**behave-dark** *https://atom.io/themes/behave-theme*      | ![Dark theme based on behave](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/behave-dark/footprint_editor.png)
**blue-green-dark**                                        | ![Dark theme using blue and green](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/blue-green-dark/footprint_editor.png)
