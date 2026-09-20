# David Mono

David Mono is an amalgamated coding font:

- JetBrains Mono supplies English, Latin, Greek, Cyrillic, symbols, and
  programming ligatures.
- Noto Sans Hebrew supplies Hebrew letters, points, cantillation marks, and
  presentation forms.

The Hebrew source uses open, near-normal Noto proportions and is optically
centered in the same 600-unit character cells as JetBrains Mono. Its scale and
rhythm are tuned to feel at home in macOS interfaces while retaining the
OFL-licensed Noto outlines. This keeps mixed English and Hebrew text aligned in
editors and terminals. Hebrew remains upright in the italic styles because
Noto Sans Hebrew has no italic source.

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
