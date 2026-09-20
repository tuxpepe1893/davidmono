#!/usr/bin/env python3
"""Validate generated David Mono desktop and web fonts."""

from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont


WEIGHTS = {
    "Thin": 100,
    "ExtraLight": 200,
    "Light": 300,
    "Regular": 400,
    "Medium": 500,
    "SemiBold": 600,
    "Bold": 700,
    "ExtraBold": 800,
}


def style_weight(style: str) -> int:
    base = "Regular" if style in {"Regular", "Italic"} else style.removesuffix(" Italic")
    return WEIGHTS[base]


def validate_ttf(path: Path) -> None:
    font = TTFont(path)
    cmap = font.getBestCmap()
    style = font["name"].getDebugName(17)
    assert font["name"].getDebugName(16) == "David Mono"
    assert font["OS/2"].usWeightClass == style_weight(style)
    assert font["post"].isFixedPitch == 1
    assert {"GDEF", "GPOS", "GSUB"} <= set(font.keys())
    assert all(codepoint in cmap for codepoint in range(0x05D0, 0x05EB))

    notice = font["name"].getDebugName(0)
    assert "JetBrains Mono Project Authors" in notice
    assert "2022 The Noto Project Authors" in notice
    assert "2024 The Noto Project Authors" in notice

    glyph_set = font.getGlyphSet()
    for codepoint in range(0x0590, 0x0600):
        glyph_name = cmap.get(codepoint)
        if not glyph_name:
            continue
        advance = font["hmtx"][glyph_name][0]
        if unicodedata.category(chr(codepoint)).startswith("M"):
            assert advance == 0, (path, hex(codepoint), advance)
        else:
            assert advance == 600, (path, hex(codepoint), advance)

    # The main alphabet must be visually centered even when bold strokes
    # overhang the nominal cell slightly.
    for codepoint in range(0x05D0, 0x05EB):
        pen = BoundsPen(glyph_set)
        glyph_set[cmap[codepoint]].draw(pen)
        assert pen.bounds is not None
        center = (pen.bounds[0] + pen.bounds[2]) / 2
        assert abs(center - 300) <= 1, (path, hex(codepoint), pen.bounds)

    for table in font.keys():
        if table != "GlyphOrder":
            font.getTableData(table)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "font_dir", nargs="?", type=Path, default=Path("fonts/david-mono")
    )
    args = parser.parse_args()

    ttf_files = sorted((args.font_dir / "ttf").glob("DavidMono-*.ttf"))
    web_files = sorted((args.font_dir / "webfonts").glob("DavidMono-*.woff2"))
    assert len(ttf_files) == 16, f"expected 16 TTF files, found {len(ttf_files)}"
    assert len(web_files) == 16, f"expected 16 WOFF2 files, found {len(web_files)}"

    for path in ttf_files:
        validate_ttf(path)
    for path in web_files:
        font = TTFont(path)
        assert font.flavor == "woff2"
        assert font["name"].getDebugName(16) == "David Mono"

    print(f"Validated {len(ttf_files)} TTF and {len(web_files)} WOFF2 fonts")


if __name__ == "__main__":
    main()
