#!/usr/bin/env python3
"""Generate the official Homebrew submission cask from the maintained tap cask.

Usage: python scripts/prepare_homebrew_cask.py /path/to/font-david-mono.rb
Generation does not establish Homebrew eligibility or submit a pull request.
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Casks" / "david-mono.rb"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="destination named font-david-mono.rb")
    args = parser.parse_args()
    if args.output.name != "font-david-mono.rb":
        parser.error("the official font cask must be named font-david-mono.rb")

    text = SOURCE.read_text()
    header = 'cask "david-mono" do\n'
    if not text.startswith(header) or not text.endswith("end\n"):
        raise SystemExit("Unexpected source cask structure; review before generating")
    text = text.replace(header, 'cask "font-david-mono" do\n', 1)
    if "# No zap stanza required" not in text:
        text = text[:-4] + "\n  # No zap stanza required\nend\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    print(f"Prepared {args.output}; Homebrew acceptance requirements still apply")


if __name__ == "__main__":
    main()
