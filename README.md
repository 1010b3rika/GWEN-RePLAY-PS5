# GWEN ▶ RePLAY™ PS5

**Author and developer: tenten1824** · Version **0.9.0**

Native PS5 gameplay recording, screenshots and controller shortcuts, with a Windows capture app and one shared local media library.

## Supported firmware

| PS5 firmware | Support |
| --- | --- |
| 7.01 | Hardware verified |
| 10.01 | Hardware verified |
| 13.20 Pro | Hardware verified |
| 13.60 | Hardware verified |

**One ELF supports these four versions.** Other firmware is rejected before capture integration. No support is claimed for 12.70 or other versions.

## Download

Get the **full package ZIP** from [Releases](https://github.com/Tenten1824/GWEN-RePLAY-PS5/releases).

- Full package: extract the ZIP and run **GWEN-RePLAY-PS5-Setup.exe**, then open **GWEN ▶ RePLAY™ PS5** from Start. The installer adds shortcuts and supports uninstalling through Windows Apps.
- ELF only: **GWEN ▶ RePLAY™ PS5.elf** is the same firmware-detecting payload for all four supported versions. Use the PC package for automatic copying and audio export.
- Source: **Source.zip** includes the native recorder, Windows launcher and Cloud service.

## Install and use

You need a Windows PC with **Python 3.12 x64**, and a supported PS5 with a working **ELF loader on port 9021** and **FTP on port 2121**. Dependency and FFmpeg wheels are bundled; the Python interpreter and jailbreak are not included.

1. Start your PS5's loader and FTP, then open your game. Put the PC and PS5 on the same private network.
2. Run the installer from the ZIP, open GWEN from Start, and enter **your PS5's IP address**.
3. Click **Video**, **Screenshot**, or **Game audio**. GWEN loads its included ELF when needed. Click Video or Game audio again to stop and save.

After a PS5 restart, start its loader/FTP and use the app again. Load one recorder instance per console; duplicate loading is blocked. The monitor has no four-hour cutoff. Sony's per-video duration limits still apply.

## Controls

| Action | Controller | Windows app |
| --- | --- | --- |
| Start/stop video | **L2 + Options/Start** | Click **Video** to start; click again to save |
| Screenshot | **R2 + Create/Select** | Click **Screenshot** |
| Separate audio-only export | PC only | Click **Game audio** to start; click again to save AAC/M4A |

Hold the trigger, press and release the second button, then release the trigger. Normal Options/Create actions still reach games and system menus. Close any pause/Create panel with the triggers released. Video and audio-only use the same native recording session, one at a time.

## Where captures go

Video and screenshots first save on the **PS5**. While the PC and PS5 FTP are available, GWEN automatically copies saved captures into your **PC library**.

Open the **Library** tile or visit **http://127.0.0.1:8787** on that PC. All your supported consoles share this library, with automatic console sections and firmware filters. Enter each console's IP in the app to add it.

“Cloud” means your local PC library here. Every user has their own library on their own PC; it does not connect to the developer's library. There is no account or password. The 100 GiB quota uses your existing PC disk space, not hosted online storage. The default location is `%LOCALAPPDATA%\GWEN RePLAY PS5\Library`.

Sony may clean temporary PS5 screenshot files; verified downloaded originals remain in the PC library. GWEN does not delete PS5 media. Audio-only exports are saved as AAC/M4A on PC; the source video remains on PS5.

## Verified scope and limits

Fresh video, screenshots, physical shortcuts, audio exports, automatic uploads, checksums, duplicate rejection and clean shutdown/reload were verified on the four listed consoles. See **GWEN-VERIFICATION.json**. Remote Play controller input and a multi-hour soak are unverified. Sony's blocked-scene and native recording restrictions apply.

The media service listens on localhost **8787**. A separate read-only payload/logo catalog uses LAN port **8790** and serves no personal media. Keep console FTP on a trusted private LAN.

If setup fails, see **CLOUD-SETUP.log** and **CLOUD-START.log** next to the app. If capture is blocked, return to gameplay and close Home/Create panels. Do not repeatedly send another ELF after an unconfirmed error.

## Credits and license

**GWEN ▶ RePLAY™ PS5** is inspired by **GWEN™ — Gaming World Entertainment Network**. GWEN™ is an independent gaming and entertainment project inspired by Gwen.

Developed by **Tenten1824** with development assistance from **OpenAI Codex**. Product direction, visual identity, custom interface and application integration: **Tenten1824**.

See **CREDITS.txt**, **NOTICE.txt**, and the **GPL-3.0-or-later LICENSE**. Preserve the original author and license notices when redistributing or modifying the project. Third-party components retain their own licenses. No private Sony firmware binaries, personal captures, saved console registry or credentials are included. The portable EXE is reserved for developer builds and is not distributed in public releases.
