#!/usr/bin/env python3
"""Validate the David Mono cask against its immutable release archive."""

from __future__ import annotations

import hashlib
import io
import re
import urllib.request
import zipfile
from pathlib import Path


cask = Path("Casks/david-mono.rb").read_text()
version = re.search(r'^  version "([^"]+)"$', cask, re.MULTILINE).group(1)
expected_sha = re.search(r'^  sha256 "([0-9a-f]{64})"$', cask, re.MULTILINE).group(1)
fonts = set(re.findall(r'^  font "([^"]+)"$', cask, re.MULTILINE))
assert len(fonts) == 16, f"expected 16 font artifacts, found {len(fonts)}"
fonts = {path.replace("#{version}", version) for path in fonts}
url = (
    f"https://github.com/tuxpepe1893/davidmono/releases/download/"
    f"v{version}/DavidMono-{version}.zip"
)
request = urllib.request.Request(url, headers={"User-Agent": "davidmono-cask-validator"})
with urllib.request.urlopen(request) as response:
    archive = response.read()
actual_sha = hashlib.sha256(archive).hexdigest()
assert actual_sha == expected_sha, (actual_sha, expected_sha)
with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
    bundled = set(bundle.namelist())
assert fonts <= bundled, sorted(fonts - bundled)
print(f"Validated David Mono {version}: {len(fonts)} fonts, sha256 {actual_sha}")
