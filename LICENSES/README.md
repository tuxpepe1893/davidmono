# License map

David Mono combines artifacts with compatible but distinct licenses:

- **SIL Open Font License 1.1 (`OFL.txt`)**: the font binaries and font design
  sources under `fonts/`, `sources/*.glyphs`, and
  `vendor/noto-sans-hebrew/NotoSansHebrew-wdth-wght.ttf`.
- **Apache License 2.0 (`LICENSES/Apache-2.0.txt`)**: source utilities,
  repository automation and David Mono documentation, except for the
  paths listed below under MIT or CC BY-SA.
- **MIT License (`LICENSES/MIT.txt`)**: `Casks/david-mono.rb`,
  `scripts/validate_cask.py`, `.github/workflows/test.yml`, and
  `.github/workflows/update-cask.yml`. These files originated in the merged
  Homebrew tap repository.
- **CC BY-SA 4.0**: `CODE_OF_CONDUCT.md`, as stated in its attribution section.

The fonts are derivatives of JetBrains Mono and Noto Sans Hebrew. Their
copyright notices and licenses are preserved in `OFL.txt`,
`THIRD_PARTY_NOTICES.md`, the vendored Noto `OFL.txt`, and the generated font
metadata. No Apple font file or outline is included in David Mono.

Historical prototype artifacts in Git history have unresolved licensing and
are excluded from the current tree and binary releases. Inherited upstream
images and ancillary project files retain their original notices; this map
does not assert new rights over third-party assets.
