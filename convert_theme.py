#!/usr/bin/env python3
"""Convert a Spicetify color.ini scheme into a Spotifast palette JSON file."""

from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
from pathlib import Path

COLOR_MAP = {
    "window": "main",
    "panel": "sidebar",
    "surface": "card",
    "surface_hover": "selected-row",
    "surface_active": "tab-active",
    "outline": "shadow",
    "text": "text",
    "secondary": "subtext",
    "dim": "misc",
    "accent": "button",
    "accent_hover": "button-active",
    "danger": "notification-error",
    "warning": "notification",
}

def parse_color(value: str, key: str) -> str:
    value = value.strip().lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", value):
        value = "".join(ch * 2 for ch in value)
    if re.fullmatch(r"[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", value):
        return "#" + value.upper()
    rgb = re.fullmatch(r"\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*", value)
    if rgb:
        channels = [int(part) for part in rgb.groups()]
        if all(0 <= part <= 255 for part in channels):
            return "#" + "".join(f"{part:02X}" for part in channels)
    raise ValueError(f"{key}: unsupported color {value!r}; expected hex or RGB")

def luminance(color: str) -> float:
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

def convert(source: Path, scheme: str | None) -> tuple[dict, str]:
    parser = configparser.ConfigParser(interpolation=None, strict=False, inline_comment_prefixes=(";",))
    parser.optionxform = str.lower
    with source.open(encoding="utf-8-sig") as handle:
        parser.read_file(handle)

    selected = scheme or ("base" if parser.has_section("base") else None)
    if selected is None:
        choices = parser.sections()
        if len(choices) == 1:
            selected = choices[0]
        else:
            raise ValueError("Choose a scheme with --scheme. Available: " + ", ".join(choices))
    if not parser.has_section(selected):
        raise ValueError(f"Scheme [{selected}] not found. Available: {', '.join(parser.sections())}")

    values = parser[selected]
    missing = [key for key in ("main", "text", "button") if key not in values]
    if missing:
        raise ValueError(f"Scheme [{selected}] is missing: {', '.join(missing)}")
    source_colors = {key: parse_color(value, key) for key, value in values.items()}
    colors = {target: source_colors[key] for target, key in COLOR_MAP.items() if key in source_colors}
    colors["on_accent"] = source_colors["text"]
    theme = {"base": "light" if luminance(source_colors["main"]) >= 0.48 else "dark", "colors": colors}
    return theme, selected

def main() -> int:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("color_ini", type=Path, help="path to Spicetify theme color.ini")
    cli.add_argument("--scheme", help="color.ini section to convert; defaults to [base] when present")
    cli.add_argument("--output", "-o", type=Path, help="output path; defaults beside color.ini")
    args = cli.parse_args()
    try:
        theme, selected = convert(args.color_ini, args.scheme)
        output = args.output or args.color_ini.with_name(f"{selected}.spotifast.json")
        output.write_text(json.dumps(theme, indent=2) + "\n", encoding="utf-8")
    except (OSError, configparser.Error, ValueError) as exc:
        print(f"convert_theme: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {output} ({selected}, {theme['base']})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
