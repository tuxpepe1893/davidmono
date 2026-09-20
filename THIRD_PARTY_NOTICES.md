# Third-party font sources

David Mono combines two font projects:

- **JetBrains Mono**, used for Latin, Greek, Cyrillic, symbols, and programming
  ligatures. Copyright 2020 The JetBrains Mono Project Authors. Licensed under
  the SIL Open Font License 1.1; see [`OFL.txt`](OFL.txt).
- **Noto Sans Hebrew**, used for the Hebrew blocks U+0590–U+05FF and
  U+FB1D–U+FB4F. Its OFL notice is Copyright 2022 The Noto Project Authors and its
  source font metadata is Copyright 2024 The Noto Project Authors. Licensed under the SIL
  Open Font License 1.1; see
  [`vendor/noto-sans-hebrew/OFL.txt`](vendor/noto-sans-hebrew/OFL.txt).

The generated family is named **David Mono** so it cannot be confused with
either upstream font.

Apple SF Hebrew was used only as a locally installed visual reference for
general scale and rhythm. No Apple font file, outline, table, name, or other
Apple asset is included in the project or release artifacts.

The upstream source utilities retain Apache 2.0 terms stated in the inherited
JetBrains Mono README (commit 1937130). The Homebrew cask and updater retain
the MIT notice from tap commit 318ba44. See `LICENSES/README.md`.

Historical Dynamic/Static prototype files were removed from the current tree
because their applicable license could not be established from their branches.
Their original commits remain in Git history for provenance; the current OFL
notice does not purport to retroactively license those historical files.

David Mono is an independent project and is not endorsed by JetBrains, Google,
the Noto project, or Apple. Upstream names identify the sources only.
