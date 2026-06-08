# Eldritch Cursors

A community-driven cursor theme based on [Volantes Cursors](https://github.com/varlesh/volantes-cursors), themed for the [Eldritch](https://github.com/eldritch-theme/eldritch) color palette.

## Variants

| Accent | Nix attribute | Color |
|---|---|---|
| Great Old One Green | `great-old-green` | `#37f499` |
| Watery Tomb Blue | `watery-tomb-blue` | `#04d1f9` |
| Pustule Pink | `pustule-pink` | `#f265b5` |
| Lovecraft Purple | `lovecraft-purple` | `#a48cf2` |
| R'lyeh Red | `rlyeh-red` | `#f16c75` |
| Dreaming Orange | `dreaming-orange` | `#f7c67f` |
| Gold of Yuggoth | `gold-of-yuggoth` | `#f1fc79` |
| Sunken Depths | `sunken-depths` | `#212337` |
| Lighthouse White | `lighthouse-white` | `#ebfafa` |

## Installation

### GitHub Release

1. Download your preferred variant from the [latest release](https://github.com/eldritch-theme/cursors/releases/latest).
2. Extract the zip to `$HOME/.local/share/icons` or `$HOME/.icons`.
3. Select the theme in your desktop environment settings.

### Nix

```nix
# All variants
pkgs.eldritch-cursors

# Single variant
pkgs.eldritch-cursors.great-old-green
```

Or build directly from the flake:

```bash
nix build github:eldritch-theme/cursors#great-old-green
```

### NixOS module

```nix
{ pkgs, ... }: {
  environment.systemPackages = [ pkgs.eldritch-cursors ];

  environment.variables.XCURSOR_THEME = "Eldritch Cthulhu Great Old Green";
}
```

### Manual build

Requirements: `python3`, `inkscape`, `xcursorgen`, `zip`.

```bash
git clone https://github.com/eldritch-theme/cursors.git
cd cursors

# Build all variants
./build -p palettes/eldritch-cthulhu.json

# Build specific accent
./build -p palettes/eldritch-cthulhu.json -a 'great-old-green'

# Built themes go to dist/
```

Or with `just`:

```bash
just build  # all variants
just single great-old-green  # single accent
```

## Acknowledgments

- [varlesh](https://github.com/varlesh/volantes-cursors) for the original Volantes Cursors.
- [catppuccin/cursors](https://github.com/catppuccin/cursors) for the approach this project is based on.
- [eldritch-theme](https://github.com/eldritch-theme/eldritch) for the color palette.

## License

GPL-3.0-only
