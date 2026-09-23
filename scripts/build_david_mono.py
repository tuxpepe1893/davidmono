#!/usr/bin/env python3
"""Build David Mono from JetBrains Mono and Noto Sans Hebrew."""

from __future__ import annotations

import argparse
import shutil
import tempfile
import unicodedata
from pathlib import Path

from fontTools import subset
from fontTools.merge import Merger
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parents[1]
JETBRAINS_DIR = ROOT / "fonts" / "ttf"
NOTO_SOURCE = ROOT / "vendor" / "noto-sans-hebrew" / "NotoSansHebrew-wdth-wght.ttf"
OUTPUT_DIR = ROOT / "fonts" / "david-mono"
FONT_VERSION = "1.003"

# Retain Noto's open proportions and proportional spacing for Hebrew text.
NOTO_WIDTH = 95.0
# Match the apparent stroke density and width of SF Hebrew's light weights
# using the redistributable Noto outlines. Keep the public style weights below.
LIGHT_HEBREW_AXES = {
    "Thin": (150, 93.0),
    "ExtraLight": (255, 93.0),
    "Light": (340, 93.0),
}
HEBREW_RANGES = ((0x0590, 0x05FF), (0xFB1D, 0xFB4F))

STYLES = (
    ("Thin", 100),
    ("ExtraLight", 200),
    ("Light", 300),
    ("Regular", 400),
    ("Medium", 500),
    ("SemiBold", 600),
    ("Bold", 700),
    ("ExtraBold", 800),
)


def hebrew_codepoints() -> set[int]:
    return {
        codepoint
        for start, end in HEBREW_RANGES
        for codepoint in range(start, end + 1)
        if unicodedata.category(chr(codepoint)) != "Cn"
    }


def hebrew_axes(style: str, weight: int) -> tuple[int, float]:
    return LIGHT_HEBREW_AXES.get(style, (weight, NOTO_WIDTH))


def make_hebrew_instance(weight: int, width: float, destination: Path) -> set[str]:
    font = TTFont(NOTO_SOURCE)
    instance = instantiateVariableFont(
        font, {"wght": weight, "wdth": width}, inplace=True
    )

    options = subset.Options()
    options.layout_features = ["*"]
    options.name_IDs = []
    options.name_legacy = False
    options.name_languages = []
    options.notdef_glyph = True
    options.notdef_outline = True
    options.recommended_glyphs = True
    options.glyph_names = True
    options.hinting = False
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=hebrew_codepoints())
    subsetter.subset(instance)

    glyphs = set(instance.getGlyphOrder()) - {".notdef", ".null", "nonmarkingreturn"}
    instance.save(destination, reorderTables=False)
    return glyphs


def set_name(font: TTFont, name_id: int, value: str) -> None:
    name = font["name"]
    name.names = [record for record in name.names if record.nameID != name_id]
    name.setName(value, name_id, 3, 1, 0x409)
    name.setName(value, name_id, 1, 0, 0)


def rename_family(font: TTFont, style: str, italic: bool) -> None:
    full_style = (
        "Italic" if style == "Regular" and italic else style + (" Italic" if italic else "")
    )
    postscript_style = full_style.replace(" ", "")

    if style in {"Regular", "Bold"}:
        legacy_family = "David Mono"
        legacy_style = "Italic" if style == "Regular" and italic else full_style
    else:
        legacy_family = f"David Mono {style}"
        legacy_style = "Italic" if italic else "Regular"

    full_name = "David Mono" if full_style == "Regular" else f"David Mono {full_style}"
    names = {
        0: (
            "JetBrains Mono glyphs copyright 2020 The JetBrains Mono Project Authors. "
            "Copyright 2022 The Noto Project Authors (https://github.com/notofonts/hebrew). "
            "Copyright 2024 The Noto Project Authors (https://github.com/notofonts/hebrew). "
            "Copyright 2026 David Mono Project Authors."
        ),
        1: legacy_family,
        2: legacy_style,
        3: f"{FONT_VERSION};DM;DavidMono-{postscript_style}",
        4: full_name,
        5: f"Version {FONT_VERSION}",
        6: f"DavidMono-{postscript_style}",
        7: "JetBrains Mono is a trademark of JetBrains s.r.o.",
        8: "David Mono contributors",
        9: "The JetBrains Mono Project Authors; The Noto Project Authors",
        10: "JetBrains Mono with Hebrew glyphs from Noto Sans Hebrew.",
        11: "https://github.com/tuxpepe1893/davidmono",
        12: "https://github.com/tuxpepe1893/davidmono",
        13: (
            "This Font Software is licensed under the SIL Open Font License, "
            "Version 1.1."
        ),
        14: "https://openfontlicense.org",
        16: "David Mono",
        17: full_style,
    }
    for name_id, value in names.items():
        set_name(font, name_id, value)


def finish_font(font: TTFont, hebrew_glyphs: set[str], style: str, weight: int, italic: bool) -> None:
    # Hebrew retains Noto advances, bearings and anchors; Latin remains monospaced.
    font["post"].isFixedPitch = 0
    font["hhea"].advanceWidthMax = max(a for a, _ in font["hmtx"].metrics.values())
    font["OS/2"].panose.bProportion = 0
    font["OS/2"].recalcAvgCharWidth(font)
    font["head"].fontRevision = float(FONT_VERSION)
    font["OS/2"].usWeightClass = weight
    font["OS/2"].usWidthClass = 5
    rename_family(font, style, italic)

    if "DSIG" in font:
        del font["DSIG"]


def build_style(style: str, weight: int, italic: bool, ttf_dir: Path, web_dir: Path) -> None:
    suffix = "Italic" if style == "Regular" and italic else style + ("Italic" if italic else "")
    source_suffix = "Italic" if style == "Regular" and italic else suffix
    source = JETBRAINS_DIR / f"JetBrainsMono-{source_suffix}.ttf"
    destination = ttf_dir / f"DavidMono-{suffix}.ttf"

    with tempfile.TemporaryDirectory(prefix="david-mono-") as temp_dir:
        hebrew_path = Path(temp_dir) / "NotoSansHebrew.ttf"
        hebrew_weight, hebrew_width = hebrew_axes(style, weight)
        hebrew_glyphs = make_hebrew_instance(hebrew_weight, hebrew_width, hebrew_path)
        source_font = TTFont(source, lazy=True)
        source_created = source_font["head"].created
        source_modified = source_font["head"].modified
        source_font.close()
        font = Merger().merge([str(source), str(hebrew_path)])
        finish_font(font, hebrew_glyphs, style, weight, italic)
        font["head"].created = source_created
        font["head"].modified = source_modified
        font.recalcTimestamp = False
        font.flavor = None
        font.save(destination, reorderTables=False)

        font.flavor = "woff2"
        font.save(web_dir / f"DavidMono-{suffix}.woff2", reorderTables=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir", type=Path, default=OUTPUT_DIR, help="directory for generated fonts"
    )
    args = parser.parse_args()

    if not NOTO_SOURCE.exists():
        raise SystemExit(f"Missing vendored source: {NOTO_SOURCE}")

    output_dir = args.output_dir.resolve()
    if output_dir.exists():
        shutil.rmtree(output_dir)
    ttf_dir = output_dir / "ttf"
    web_dir = output_dir / "webfonts"
    ttf_dir.mkdir(parents=True)
    web_dir.mkdir(parents=True)

    for style, weight in STYLES:
        for italic in (False, True):
            build_style(style, weight, italic, ttf_dir, web_dir)
            print(f"Built DavidMono-{style}{'Italic' if italic else ''}")


if __name__ == "__main__":
    main()
