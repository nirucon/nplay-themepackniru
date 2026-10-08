#!/usr/bin/env python3
"""Install/validate/uninstall NPLAY NIRU theme pack without touching NPLAY user data."""
import argparse
import hashlib
import os
from pathlib import Path
import re
import sys
import tomllib

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "themes"
NAME = re.compile(r"^[a-z][a-z0-9-]{0,47}$")
COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")
KEYS = {"fg", "muted", "accent", "bg", "select_fg", "select_bg"}
BUILTINS = {"niru-noir", "satie", "c-larsson", "hackerman", "commodore64", "othala", "ingwaz", "omarchy"}

def destination():
    config = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))).expanduser()
    return config / "nplay" / "themes"

def files():
    return sorted(SOURCE.glob("*.toml"))

def validate(path):
    if path.is_symlink() or path.stat().st_size > 16384:
        raise ValueError("Symlink or oversized theme")
    with path.open("rb") as stream:
        doc = tomllib.load(stream)
    if set(doc) != {"theme", "colors"}:
        raise ValueError("Expected [theme] and [colors]")
    meta, colors = doc["theme"], doc["colors"]
    if not isinstance(meta, dict) or not isinstance(colors, dict):
        raise ValueError("Invalid TOML sections")
    ident = meta.get("id")
    if not isinstance(ident, str) or not NAME.fullmatch(ident) or ident != path.stem or ident in BUILTINS:
        raise ValueError("Invalid or reserved theme ID")
    if set(meta) - {"id", "name", "author", "version"} or not colors or set(colors) - KEYS:
        raise ValueError("Unknown field or missing colors")
    if any(not isinstance(v, str) or not COLOR.fullmatch(v) for v in colors.values()):
        raise ValueError("Colors must be #RRGGBB")
    label = meta.get("name", ident)
    if not isinstance(label, str) or not 1 <= len(label) <= 48 or any(ord(c) < 32 for c in label):
        raise ValueError("Invalid label")
    return label

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(action):
    items = files()
    if len(items) != 5:
        raise RuntimeError(f"Expected exactly 5 themes; found {len(items)}")
    for item in items:
        validate(item)
    if action == "check":
        print("PASS: 5 valid NPLAY 1.4.1 theme files")
        return
    target_dir = destination()
    if target_dir.is_symlink():
        raise RuntimeError(f"Refusing symlink theme directory: {target_dir}")
    if action == "install":
        target_dir.mkdir(parents=True, exist_ok=True)
    elif not target_dir.is_dir():
        print("No installed theme directory; nothing to remove.")
        return
    for source in items:
        target = target_dir / source.name
        if action == "install":
            try:
                # Exclusive creation prevents overwriting user-modified themes.
                with target.open("xb") as handle:
                    handle.write(source.read_bytes())
                print(f"INSTALLED {source.name}")
            except FileExistsError:
                print(f"SKIPPED   {source.name} (already exists)")
        else:
            if target.is_symlink() or not target.is_file():
                print(f"SKIPPED   {source.name} (missing or not a regular file)")
            elif digest(target) != digest(source):
                print(f"SKIPPED   {source.name} (modified; kept safely)")
            else:
                target.unlink()
                print(f"REMOVED   {source.name}")
    print("NPLAY → Settings → Appearance → Theme → RELOAD CUSTOM THEMES")

def main():
    parser = argparse.ArgumentParser(description="NPLAY Theme Pack NIRU 1.0.0")
    parser.add_argument("action", choices=["check", "install", "uninstall"])
    args = parser.parse_args()
    try:
        run(args.action)
    except (OSError, ValueError, tomllib.TOMLDecodeError, RuntimeError) as exc:
        parser.exit(1, f"ERROR: {exc}\n")

if __name__ == "__main__":
    main()
