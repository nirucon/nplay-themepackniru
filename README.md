# NPLAY Theme Pack NIRU

**Five original Norse-inspired palettes for NPLAY 1.4.1+**, designed by Ing Leif Nicklas Rudolfsson.

An independent theme collection for the NPLAY Linux terminal music player. Designed for a calm, legible, atmospheric appearance in Kitty and other 256-color terminals. Every palette is an original interpretation, not a copy of an existing editor theme.

## The collection

| Theme | Mood | Background | Accent |
|---|---|---|---|
| **Odin** | Raven-black stone, weathered gold, silver | `#111416` | `#D7B36A` |
| **Nifelheim** | Frozen abyss and cold blue light | `#0B1924` | `#8FD5EA` |
| **Yggdrasil** | Old forest, moss, bark and soft daylight | `#141D18` | `#A9C77A` |
| **Urdr** | Night violet, ivory and threads of fate | `#1A1720` | `#D7A0B7` |
| **Runes** | Dark runestone, copper and ancient parchment | `#211C1B` | `#DF9063` |

The five palettes have deliberately different atmospheres while keeping NPLAY's accent, selection, foreground and muted text readable.

## Requirements

- NPLAY **1.4.1 or later** with custom TOML themes
- Python **3.11+** for the optional installer
- Terminal with **256 colors** recommended (Kitty works well)

## Install

Extract this release and run:

```sh
python3 manage.py check
bash install.sh
```

The five files are copied into `${XDG_CONFIG_HOME:-$HOME/.config}/nplay/themes/`. Existing files are **never overwritten**. You can also install one theme by copying its `.toml` file manually.

In NPLAY, navigate to **Settings → Appearance → Theme → RELOAD CUSTOM THEMES**, then choose Odin, Nifelheim, Yggdrasil, Urdr or Runes. Reopen the theme menu if necessary.

## Verify

```sh
nplay --list-themes
nplay --check-theme "${XDG_CONFIG_HOME:-$HOME/.config}/nplay/themes/odin.toml"
```

## Remove

```sh
bash uninstall.sh
```

Only unchanged files distributed by this pack are removed. Modified palettes are retained. Your music, Spotify configuration, playlists, database, and other NPLAY themes are not touched.

## Design and compatibility

NPLAY currently supports six semantic fields: `fg`, `muted`, `accent`, `bg`, `select_fg`, `select_bg`. All five are complete, self-contained TOML themes. There are no executable theme scripts or application patches.

NPLAY uses terminal approximations of RGB values on 256-color terminals, so the displayed shade may differ slightly from these hex codes. See `PREVIEW.png` for intended palette relationships; it is an illustrative reference rather than a screenshot from NPLAY.

## Version

**1.0.0** — first release, five original palettes.

## License

The pack's original code, documentation and color configurations are MIT licensed. © 2026 Nicklas Rudolfsson. See `LICENSE`.
