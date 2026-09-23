#!/usr/bin/env python3
"""Check that a rebuild has the same font data as the committed artifacts."""

from __future__ import annotations

import argparse
from io import BytesIO
from pathlib import Path

from fontTools.ttLib import TTFont


FORMATS = (("ttf", "*.ttf"), ("webfonts", "*.woff2"))


def table_xml(font: TTFont, tag: str) -> bytes:
    output = BytesIO()
    font.saveXML(output, tables=[tag])
    return output.getvalue()


def compare_font(expected_path: Path, rebuilt_path: Path) -> None:
    expected = TTFont(expected_path)
    rebuilt = TTFont(rebuilt_path)
    try:
        assert expected.sfntVersion == rebuilt.sfntVersion, expected_path
        assert expected.getGlyphOrder() == rebuilt.getGlyphOrder(), expected_path
        assert set(expected.keys()) == set(rebuilt.keys()), expected_path

        # The whole-font checksum changes when equivalent layout tables have
        # different binary encodings, so compare its normalized value.
        expected["head"].checkSumAdjustment = 0
        rebuilt["head"].checkSumAdjustment = 0
        for tag in expected.keys():
            if tag == "GlyphOrder":
                continue
            if expected.getTableData(tag) != rebuilt.getTableData(tag):
                assert table_xml(expected, tag) == table_xml(rebuilt, tag), (
                    expected_path,
                    tag,
                )
    finally:
        expected.close()
        rebuilt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("rebuilt", type=Path)
    args = parser.parse_args()

    total = 0
    for folder, pattern in FORMATS:
        expected = sorted((args.expected / folder).glob(pattern))
        rebuilt = sorted((args.rebuilt / folder).glob(pattern))
        assert len(expected) == len(rebuilt) == 16, folder
        assert [p.name for p in expected] == [p.name for p in rebuilt], folder
        for expected_path, rebuilt_path in zip(expected, rebuilt):
            compare_font(expected_path, rebuilt_path)
            total += 1
    print(f"Verified equivalent font data in {total} rebuilt files")


if __name__ == "__main__":
    main()
