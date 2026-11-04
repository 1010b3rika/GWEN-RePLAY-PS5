# Release assembly

Author and developer: 1010B3rika.

The seed parts contain the audited runtime, precompiled hardware-verified ELF, Windows launcher, source archive and branding. seed.json verifies every part and the complete seed. The workflow retrieves dependency wheels from PyPI only when their SHA-256 matches the original audited wheel in wheels.json, verifies the Windows launcher points to the unchanged native ELF, and publishes version 0.9.2. No Sony firmware binaries or personal captures are included.

To inspect source locally, concatenate seed/part-*.bin in listed order, verify the complete hash in seed.json, open the resulting ZIP and extract Source.zip. Native source rebuild instructions are in Source.zip/BUILD.txt. The included source was locally rebuilt to the same native ELF SHA-256.

Portable EXE binaries are developer-only and are not published.

The public ZIP includes an Inno Setup installer and open source. CI verifies actual installation and uninstallation in an isolated runner-temp folder before publication.


The public installer includes an isolated CPython 3.12 x64 runtime and verified dependencies. No system Python is needed. CI removes Python from PATH, uses an empty user profile, validates the bundled interpreter and setup, then starts the real local gallery with a temporary empty library and no console connections. It verifies HTTP health, gallery loading and clean shutdown before publishing.
