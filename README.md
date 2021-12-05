# kicad-color-schemes

Want to change the color scheme of KiCad? Look here for inspiration.

## Install Color Themes using the PCM (KiCad 5.99 demo feature)

If you run KiCad 5.99 which was build including the new Plugin and Content Manager (using the compile option `-DKICAD_PCM=ON`), you can simply add the repository url and install the themes inside KiCad:
- https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/repository.json

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

| color-scheme                                               | screenshot                                                                                                                                  |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **kicad-classic**                                          | ![Default theme for KiCad 5.x and earlier](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-classic/eeschema.png) |
| **kicad-2020**                                             | ![Default theme for KiCad 6.0](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-2020/eeschema.png)                |
| **solarized-dark** *http://ethanschoonover.com/solarized*  | ![Dark theme based on solarized](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/solarized-dark/eeschema.png)          |
| **solarized-light** *http://ethanschoonover.com/solarized* | ![Light theme based on solarized](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/solarized-light/eeschema.png)        |
| **black-white**                                            | ![simple black/white theme](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/black-white/eeschema.png)                  |
| **blue-tone**                                              | ![Blue tone theme](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/blue-tone/eeschema.png)                             |
| **behave-dark** *https://atom.io/themes/behave-theme*      | ![Dark theme based on behave](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/behave-dark/eeschema.png)                |
| **neon** *Inspired by forum user BobZ*                     | ![Neon coloured theme inspired by forum user BobZ](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/neon/eeschema.png)  |
| **nord** *Designed by @0xdec*                              | ![based on the nordtheme color palette](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/nord/eeschema.png)             |
| **monokai** *Inspired by forum user kickofighto*           | ![Dark theme based on monokai](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/monokai/eeschema.png)                   |
| **eagle-dark** *Designed by DX-MON, Inspired by EagleCAD*  | ![Dark theme based on Eagle](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/eagle-dark/eeschema.png)                  |
| **wdark** *Designed by wykys, Inspired by One Dark*        | ![Dark theme designed for schematic editor](wdark/eeschema.png)                                                                             |
| **wlight** *Designed by wykys, Inspired by Altium*         | ![Light theme designed for export to PDF](wlight/eeschema.png)                                                                              |

## pcbnew
| color-scheme                                              | screenshot                                                                                                                                |
| --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **kicad-classic**                                         | ![Default theme for KiCad 5.x and earlier](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-classic/pcbnew.png) |
| **kicad-2020**                                            | ![Default theme for KiCad 6.0](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-2020/pcbnew.png)                |
| **behave-dark** *https://atom.io/themes/behave-theme*     | ![Dark theme based on behave](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/behave-dark/pcbnew.png)                |
| **blue-green-dark**                                       | ![Dark theme using blue and green](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/blue-green-dark/pcbnew.png)       |
| **nord** *Designed by @0xdec*                             | ![based on the nordtheme color palette](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/nord/pcbnew.png)             |
| **eagle-dark** *Designed by DX-MON, Inspired by EagleCAD* | ![Loosely based on Eagle's dark theme](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/eagle-dark/pcbnew.png)        |

## footprint editor
| color-scheme                                              | screenshot                                                                                                                                          |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **kicad-classic**                                         | ![Default theme for KiCad 5.x and earlier](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-classic/footprint_editor.png) |
| **kicad-2020**                                            | ![Default theme for KiCad 6.0](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/kicad-2020/footprint_editor.png)                |
| **behave-dark** *https://atom.io/themes/behave-theme*     | ![Dark theme based on behave](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/behave-dark/footprint_editor.png)                |
| **blue-green-dark**                                       | ![Dark theme using blue and green](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/blue-green-dark/footprint_editor.png)       |
| **nord** *Designed by @0xdec*                             | ![based on the nordtheme color palette](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/nord/footprint_editor.png)             |
| **eagle-dark** *Designed by DX-MON, Inspired by EagleCAD* | ![Loosely based on Eagle's dark theme](https://raw.githubusercontent.com/pointhi/kicad-color-schemes/master/eagle-dark/footprint_editor.png)        |
