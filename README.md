# Spicetify to Spotifast Colors

Convert a Spicetify theme's `color.ini` color scheme into a Spotifast custom color palette (`.json`).

**Colors only.** This tool does not convert or run Spicetify extensions, CSS snippets, custom apps, or CSS/JavaScript theme features. It does not change Spotify credentials or playback behavior.

## Use it

1. Install Python 3.10 or newer.
2. Find the `color.ini` in the Spicetify theme folder.
3. Run this in PowerShell, replacing the path and scheme as needed:

```powershell
py convert_theme.py C:\path\to\Theme\color.ini --scheme dracula
```

Use a section name from the file (for example, `dracula`, `nord-dark`, or `catppuccin-mocha`). When `--scheme` is omitted, the converter uses `[base]` if present. The converter writes `<scheme>.spotifast.json` beside `color.ini`. To choose a location, add `--output C:\path\to\my-theme.json`.

4. In Spotifast, open **Settings → Appearance → Theme → Open themes folder** and copy the JSON there.
5. Run `spotifast reload-themes` if Spotifast is already open, then select the palette under **Settings → Appearance → Theme**.

Spotifast's custom palettes change colors and keep its existing fonts. See [Spotifast's theme guide](https://github.com/crmne/spotifast/blob/main/docs/_reference/settings-and-files.md#custom-themes).

## Color mapping

| Spicetify `color.ini` | Spotifast palette |
| --- | --- |
| main | window |
| sidebar | panel |
| card | surface |
| selected-row | surface_hover |
| tab-active | surface_active |
| shadow | outline |
| text | text, on_accent |
| subtext | secondary |
| misc | dim |
| button | accent |
| button-active | accent_hover |
| notification-error | danger |
| notification | warning |

The converter accepts 3, 6, or 8 digit hex colors (with or without `#`) and comma separated RGB values. It estimates `light` or `dark` from the `main` color. Unsupported values such as unresolved CSS variables cause an error.

## Limits

Spicetify themes can include CSS that changes Spotify's layout, JavaScript, and integrations. Those features are outside this converter's scope. Spotifast is a native Rust/egui app; Spicetify extensions such as Spicy Lyrics cannot run in it, and this project does not add a plugin API or lyrics menu.

## Credit

Code implementation: OpenAI Codex. Repository owner and publisher: SwordPro41.
