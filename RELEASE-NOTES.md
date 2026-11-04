# GWEN â–¶ RePLAYâ„¢ PS5 v0.9.2

**Author and developer: 1010B3rika**

**GWEN â–¶ RePLAYâ„¢ PS5** is inspired by **GWENâ„¢ â€” Gaming World Entertainment Network**. GWENâ„¢ is an independent gaming and entertainment project inspired by Gwen. Developed by **1010B3rika** with development assistance from **OpenAI Codex**. Product direction, visual identity, custom interface and application integration: **1010B3rika**.

Public installer fix: bundles an isolated CPython runtime and all dependencies. Fixes startup on PCs without Python or with the Microsoft Store Python alias. The app requires no separate Python setup. Startup is checked with system Python unavailable. This update does not change the ELF, capture bridge, shortcuts or firmware support.

One firmware-detecting ELF for PS5 **7.01, 10.01, 13.20 Pro and 13.60** only.
One shared local Cloud library at **http://127.0.0.1:8787** on your Windows PC.

- L2 + Options/Start: video start/stop and save.
- R2 + Create/Select: screenshot.
- Click Video, Screenshot or Game audio in the PC app. Audio-only starts/stops on PC.
- Saved media copies automatically while your PC and PS5 FTP are available.
- Automatic console sections and firmware filters; one library for all consoles.
- Duplicate ELF loading is blocked before ShellUI access.
- Scoped Mono attachment fixes the shutdown path; clean shutdown/reload and separate GC checks passed on all four owned consoles.

Extract the ZIP, run **GWEN-RePLAY-PS5-Setup.exe**, open GWEN from Start, enter **your PS5 IP**, and click a capture tile with your game open. Keep your console's ELF loader and FTP running. Python 3.12 x64, dependencies and FFmpeg are bundled; no separate Python setup is needed. Load the recorder again after a PS5 restart; no four-hour worker cutoff.

Cloud uses your own PC disk, with a 100 GiB quota; it is not hosted online storage. No account is required. 127.0.0.1 always refers to the PC opening the library. Each user gets their own library. The media service is loopback-only; the read-only payload/logo catalog uses LAN port 8790. Keep PS5 FTP on a trusted private LAN.

Hardware verified on the four listed firmwares. Other firmware is rejected. Remote Play input and multi-hour soak are unverified. Native blocked-scene and per-video limits apply. Sony may clean temporary PS5 screenshots; downloaded originals remain in the PC library. Options/Create inputs are not suppressed.

The package includes compiled ELF and Windows GUI applications, source code and GPL-3.0 license. It contains no jailbreak, private Sony firmware binaries, personal captures, credentials, saved console registry or developer library. See GWEN-VERIFICATION.json for the verification scope.

The portable EXE is reserved for developer builds and is excluded from this public release.

The ZIP includes the installer and open source. Preserve original author attribution and license notices when redistributing or modifying; see NOTICE.txt.



Developer attribution refresh: **1010B3rika**. ELF and Windows launcher rebuilt for the name change only. Firmware worker files are unchanged; the renamed ELF has not been hardware-retested. Earlier functional verification applies to the original binary, retained in the saved restore point.
