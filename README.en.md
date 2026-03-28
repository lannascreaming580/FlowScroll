<div align="center">

# <img src="FlowScroll/resources/FlowScroll.svg" width="40" align="center" alt="Logo" /> FlowScroll

**Global infinite scrolling with your mouse middle button**

Bring browser-style auto-scroll to your whole desktop.

`English` | [中文](README.md)

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Release](https://img.shields.io/github/v/release/CyrilPeng/FlowScroll?color=success&label=Release)]()
[![Current Version](https://img.shields.io/badge/Current%20Version-v1.5.3-2563EB.svg)]()

</div>

---

## Overview

FlowScroll extends browser middle-button auto-scroll to desktop apps.

It is designed for long pages, documents, code, timelines, and wide content where frequent wheel scrolling or dragging scrollbars is inefficient.

Typical use cases:

- Reading long web pages, docs, and PDFs
- Browsing code/log/config files
- Navigating wide sheets, canvases, and timelines
- Reducing repetitive wheel and scrollbar operations

---

## Screenshots

### Main UI

<div align="center">
  <img src="https://git-pictures.cyrilworkshop.dpdns.org/flowscroll/1.jpg" alt="Main UI" width="30%" style="margin-right: 2%;">
  <img src="https://git-pictures.cyrilworkshop.dpdns.org/flowscroll/2.jpg" alt="Settings UI" width="30%" style="margin-right: 2%;">
  <img src="https://git-pictures.cyrilworkshop.dpdns.org/flowscroll/3.jpg" alt="Work Mode" width="30%">
</div>

### Demo

<div align="center">
<img src="https://git-pictures.cyrilworkshop.dpdns.org/flowscroll/demo1.gif" alt="FlowScroll Demo 1" width="80%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
<br>
<br>
<img src="https://git-pictures.cyrilworkshop.dpdns.org/flowscroll/demo2.gif" alt="FlowScroll Demo 2" width="80%" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
</div>

---

## Download and Install

Get the latest build from [Releases](https://github.com/CyrilPeng/FlowScroll/releases).

| Platform | File | Installation |
| :--- | :--- | :--- |
| **Windows** | `FlowScroll_Win_v*.exe` | Double-click to run |
| **macOS** | `FlowScroll_Mac_v*.dmg` | Drag into `Applications`; grant Accessibility permission |
| **Linux (Preview)** | `FlowScroll_Linux_x86_v*.AppImage` | `chmod +x` then run |

Platform status:

- **Windows**: fully supported (recommended)
- **macOS**: supported, requires Accessibility permission
- **Linux**: preview; works on X11/Xorg, not available on Wayland due to global-input restrictions

---

## Quick Start

FlowScroll supports two activation modes. Each mode has its own activation hotkey/button. If empty, middle mouse button is used by default.

### Click to toggle (default)

1. Press the activation key/button once.
2. Crosshair appears, indicating scrolling mode is active.
3. Move mouse away from center to scroll (farther means faster).
4. Press activation key/button again to exit.

### Hold to activate

1. Hold the activation key/button.
2. Crosshair appears and scrolling mode activates.
3. Keep holding while moving mouse to scroll.
4. Release to exit automatically.

---

## Features

- Global scrolling interaction in common scrollable apps
- Direction indicator overlay and clear activation state
- Tunable motion curve, base speed, and dead zone
- Optional 360-degree scrolling for horizontal content
- Fullscreen disable and app filter rules (blacklist/whitelist)
- Optional WebDAV sync for presets/config
- Optional inertia scroll after release
- Independent X/Y reverse direction settings

---

## Configuration

### Built-in Presets

Includes 4 built-in presets for common scenarios:

- Web Reading
- Coding/Office
- Long Docs/Sheets (default)
- Gentle/Trackpad-like

You can save custom presets in the app. Config is stored at `~/.FlowScroll_config.json`.

### Core Parameters

- **Sensitivity curve**: controls acceleration growth
- **Speed factor**: global speed multiplier
- **Dead zone**: center area without scroll output
- **Horizontal mode**: allow X-axis scrolling
- **Inertia**: friction and trigger threshold

---

## Permissions

### macOS

FlowScroll needs Accessibility permission to listen to global input events.

### Windows

Usually no admin privilege is required.

### Linux

Global hooks are available on X11/Xorg. Wayland does not allow this class of global interception.

---

## Privacy

- Default mode is local-only
- WebDAV sync is opt-in
- Password is stored in system keychain when available
- Password is not included in preset export/sync payload

---

## Known Compatibility Notes

- macOS fullscreen detection has limitations in some apps
- Wayland is not supported for global input hooks
- Some special/UWP apps may have input hook limitations on Windows

---

## FAQ

### Will it conflict with browser middle-button auto-scroll?

No. FlowScroll targets global interaction outside browser-native behavior and supports app-level filtering.

### Blacklist vs whitelist?

- **Blacklist**: disable FlowScroll in matched apps
- **Whitelist**: enable FlowScroll only in matched apps

### How are app keywords matched?

Case-insensitive substring match against foreground window/app name.

### Why does it sometimes look inactive?

Check activation mode/hotkey, app filter rules, fullscreen disable setting, and required permissions.

### Is WebDAV password uploaded?

No. Password is kept in local secure storage and excluded from sync payload.

---

## Build from Source

```bash
git clone https://github.com/CyrilPeng/FlowScroll.git
cd FlowScroll
uv sync
uv run python main.py
```

Run tests:

```bash
uv run python -m pytest tests/ -v
```

---

## License

GPL-3.0. See [LICENSE](LICENSE).
