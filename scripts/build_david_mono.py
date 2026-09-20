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

# A near-normal width retains Noto's open proportions. Spacing glyphs are
# optically centered below so wider Hebrew forms still fit the 600-unit cell.
NOTO_WIDTH = 95.0
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


def shift_anchor(anchor: object | None, amount: int) -> None:
    if anchor is not None:
        anchor.XCoordinate += amount


def shift_gpos_base_anchors(font: TTFont, shifts: dict[str, int]) -> None:
    """Keep mark anchors aligned after spacing glyphs are centered."""
    if "GPOS" not in font:
        return

    for lookup in font["GPOS"].table.LookupList.Lookup:
        for subtable in lookup.SubTable:
            if lookup.LookupType == 4:  # Mark-to-base positioning
                for glyph_name, record in zip(
                    subtable.BaseCoverage.glyphs, subtable.BaseArray.BaseRecord
                ):
                    amount = shifts.get(glyph_name, 0)
                    for anchor in record.BaseAnchor:
                        shift_anchor(anchor, amount)
            elif lookup.LookupType == 5:  # Mark-to-ligature positioning
                for glyph_name, attachment in zip(
                    subtable.LigatureCoverage.glyphs,
                    subtable.LigatureArray.LigatureAttach,
                ):
                    amount = shifts.get(glyph_name, 0)
                    for component in attachment.ComponentRecord:
                        for anchor in component.LigatureAnchor:
                            shift_anchor(anchor, amount)
            elif lookup.LookupType == 6:  # Mark-to-mark positioning
                for glyph_name, record in zip(
                    subtable.Mark2Coverage.glyphs, subtable.Mark2Array.Mark2Record
                ):
                    amount = shifts.get(glyph_name, 0)
                    for anchor in record.Mark2Anchor:
                        shift_anchor(anchor, amount)


def center_spacing_glyphs(font: TTFont, glyph_names: set[str]) -> None:
    """Optically center Hebrew spacing glyphs in JetBrains Mono's cell."""
    glyf = font["glyf"]
    shifts: dict[str, int] = {}

    for glyph_name in sorted(glyph_names):
        advance, side_bearing = font["hmtx"][glyph_name]
        if not advance:
            continue

        glyph = glyf[glyph_name]
        glyph.expand(glyf)
        glyph.recalcBounds(glyf)
        if not hasattr(glyph, "xMin") or (
            not hasattr(glyph, "components") and not hasattr(glyph, "coordinates")
        ):
            continue
        amount = round(300 - (glyph.xMin + glyph.xMax) / 2)
        shifts[glyph_name] = amount

        if hasattr(glyph, "components"):
            for component in glyph.components:
                component.x += amount
        else:
            glyph.coordinates.translate((amount, 0))
        glyph.recalcBounds(glyf)
        font["hmtx"][glyph_name] = (600, side_bearing + amount)

    shift_gpos_base_anchors(font, shifts)


def make_hebrew_instance(weight: int, destination: Path) -> set[str]:
    font = TTFont(NOTO_SOURCE)
    instance = instantiateVariableFont(
        font, {"wght": weight, "wdth": NOTO_WIDTH}, inplace=True
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
    center_spacing_glyphs(instance, glyphs)
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
        3: f"1.001;DM;DavidMono-{postscript_style}",
        4: full_name,
        5: "Version 1.001",
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
    # Keep marks at zero advance and make every spacing Hebrew glyph occupy the
    # same 600-unit cell as JetBrains Mono.
    for glyph_name in hebrew_glyphs:
        if glyph_name in font["hmtx"].metrics:
            advance, side_bearing = font["hmtx"][glyph_name]
            if advance:
                font["hmtx"][glyph_name] = (600, side_bearing)

    font["post"].isFixedPitch = 1
    font["hhea"].advanceWidthMax = 600
    font["OS/2"].xAvgCharWidth = 600
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
        hebrew_glyphs = make_hebrew_instance(weight, hebrew_path)
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
