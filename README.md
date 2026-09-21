# David Mono

[![Build fonts](https://github.com/tuxpepe1893/davidmono/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/tuxpepe1893/davidmono/actions/workflows/build.yml)

David Mono combines JetBrains Mono for English, Latin, Greek, Cyrillic, symbols
and programming ligatures with Noto Sans Hebrew for Hebrew letters and marks.

Hebrew uses natural proportional spacing: narrow letters have compact advances,
and wide letters have room to breathe. Noto's original side bearings and mark
anchors are preserved. English remains monospaced; Hebrew text no longer follows
a fixed column grid. No Apple font data is used in the font.

Hebrew remains upright in italic styles because Noto Sans Hebrew has no italic
source.

## Install

Install the files from [`fonts/david-mono/ttf`](fonts/david-mono/ttf). Remove an
older David Mono installation first so the operating system does not retain a
cached copy.

For CSS, use the WOFF2 files in
[`fonts/david-mono/webfonts`](fonts/david-mono/webfonts).

## Homebrew

Install all desktop styles from this repository as a custom tap:

```console
brew tap tuxpepe1893/davidmono https://github.com/tuxpepe1893/davidmono
brew trust tuxpepe1893/davidmono
brew install --cask david-mono
```

Upgrade after a new release:

```console
brew update
brew upgrade --cask david-mono
```

The cask is validated in CI. A scheduled workflow checks new releases and opens
an owner-reviewed pull request when its version or checksum changes.

## Build

Use Python 3.10 or newer:

```console
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_david_mono.py
```

The build produces 16 static TTF fonts and 16 matching WOFF2 fonts, from Thin
through ExtraBold in upright and italic styles.

The inputs are the checked-in JetBrains Mono TTF files and the pinned Noto Sans
Hebrew variable font under `vendor/noto-sans-hebrew`. See
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for provenance and license
details.

## Issues and pull requests

Issues and pull requests created with AI assistance are welcome. Before opening
one, manually review the entire submission for accuracy, relevance, clarity,
and any unintended or sensitive content. For pull requests, also review and
understand every proposed change and run the project validation checks.

## License

David Mono is distributed under the
[SIL Open Font License 1.1](OFL.txt), the same license used by both upstream
fonts. It permits use, study, modification, redistribution, embedding, and
commercial use subject to the OFL conditions. See
[`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) for upstream attribution.
Source utilities and Homebrew automation retain their upstream Apache 2.0 or
MIT terms. See [`LICENSES/README.md`](LICENSES/README.md) for the per-path
license map.

Contributions are welcome. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) before participating.
