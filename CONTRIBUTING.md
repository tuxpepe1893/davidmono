# Contributing to David Mono

Thank you for helping improve David Mono.

## Code of Conduct

Participation in this project is governed by the
[Contributor Covenant 3.0](CODE_OF_CONDUCT.md).

## Development

Create a Python environment, install the build dependencies, and rebuild the
font family:

```console
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_david_mono.py
```

Before submitting a change:

1. Build all TTF and WOFF2 files without errors.
2. Run `.venv/bin/python scripts/validate_david_mono.py`.
3. Check Latin and Hebrew text, including pointed Hebrew and programming
   ligatures.
4. Describe any visual or metric changes in the pull request.
5. Update attribution when introducing material from another font project.

## Licensing contributions

Font binaries, outlines, and font design sources are Font Software under the
SIL Open Font License 1.1. Source utilities and project automation use Apache
2.0 or MIT as described in [`LICENSES/README.md`](LICENSES/README.md). By
submitting a contribution, you agree that it may be distributed under the
license assigned to that path and confirm that you have the right to submit
it. Do not contribute font outlines, artwork, code, or other material with
incompatible terms.

The Code of Conduct text is separately licensed under CC BY-SA 4.0 as described
in its attribution section.
