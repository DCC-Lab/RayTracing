# Building a standalone Raytracing app

The GUI launched by `python -m raytracing -a` can be bundled into a
double-clickable application so end users don't need to install Python
or any dependencies. This is done with
[PyInstaller](https://pyinstaller.org/).

## One-time setup

From the repo root, in the project's virtual environment:

```bash
pip install pyinstaller
```

Make sure the runtime dependencies are also installed in the same
environment, since PyInstaller freezes whatever is importable there:

```bash
pip install -e .        # raytracing itself
pip install mytk pyperclip pillow
```

## Build

From the repo root:

```bash
pyinstaller --windowed --name Raytracing --noconfirm \
    --collect-submodules PIL \
    --distpath packaging/dist --workpath packaging/build \
    raytracing/ui/raytracing_app.py
```

The result lands in `packaging/dist/`:

- **macOS**: `Raytracing.app` — a standard `.app` bundle. Double-click
  to launch, drag into `/Applications` to install.
- **Windows**: `Raytracing/Raytracing.exe` inside a folder with all
  DLLs. Zip the folder for distribution.
- **Linux**: `Raytracing/Raytracing` binary inside a folder. Users run
  the binary directly.

Typical build time: ~1 minute. Typical bundle size: ~270 MB (numpy,
matplotlib, and scipy dominate).

## Flags explained

- `--windowed` — on macOS/Windows, suppresses the terminal console
  window that would otherwise open alongside the GUI.
- `--name Raytracing` — sets the app/executable name.
- `--noconfirm` — overwrites a previous build without prompting.
- `--distpath` / `--workpath` — keeps build artifacts inside
  `packaging/` instead of scattering `build/` and `dist/` folders at
  the repo root.
- `--collect-submodules PIL` — `mytk` loads `PIL.ImageDraw` and
  `PIL.ImageTk` via `importlib.import_module()`, which PyInstaller's
  static analyzer cannot follow. Without this flag, the bundled app
  prompts the user to "install the missing module 'ImageDraw'" on
  first launch.

## Per-platform notes

PyInstaller **does not cross-compile**. To ship a Windows `.exe`, run
the build on Windows; to ship a macOS `.app`, run it on macOS; same
for Linux. Apple Silicon builds run on Apple Silicon; Intel builds
need an Intel Mac (or `arch -x86_64` + an x86_64 Python).

### macOS code signing and notarization

The unsigned `.app` will trigger Gatekeeper warnings. For distribution
outside your own machine, sign and notarize it:

```bash
codesign --deep --force --sign "Developer ID Application: NAME (TEAMID)" \
    packaging/dist/Raytracing.app
xcrun notarytool submit packaging/dist/Raytracing.app \
    --apple-id you@example.com --team-id TEAMID --wait
xcrun stapler staple packaging/dist/Raytracing.app
```

Without a Developer ID, users can still run the app by right-clicking
and choosing *Open* on first launch.

### Windows

On Windows, replace `--windowed` with `--noconsole` (same effect), and
consider `--icon app.ico` to set the executable icon. For a proper
installer, wrap the `dist/Raytracing` folder with
[Inno Setup](https://jrsoftware.org/isinfo.php) or NSIS.

## Automated builds for all three platforms

`.github/workflows/build-app.yml` builds macOS, Windows, and Linux
bundles on GitHub Actions. Two triggers:

- **Push a `v*` tag** — builds all three, attaches the zips/tarball to
  the GitHub Release for that tag.
- **Actions → "Build standalone app" → "Run workflow"** — manual
  trigger, downloads available under the run's Artifacts section.

Artifacts produced:

- `Raytracing-macOS.zip` — contains `Raytracing.app` (Apple Silicon).
  Built on `macos-14`; for Intel Macs, change the matrix entry to
  `macos-13` or add both.
- `Raytracing-Windows.zip` — contains a `Raytracing/` folder with
  `Raytracing.exe` plus its DLLs.
- `Raytracing-Linux.tar.gz` — contains a `Raytracing/` folder with the
  executable, built against Ubuntu 22.04's glibc.

The workflow installs Tk on Linux (`python3-tk`), runs the same
PyInstaller command shown above, and does no code signing. Unsigned
macOS builds will still prompt Gatekeeper; see the signing section
above if you need a signed distribution.

## Alternative: install from PyPI

For technical users, the simplest "deployment" is still:

```bash
pip install raytracing mytk pyperclip
python -m raytracing -a
```

Use the PyInstaller bundle when the audience cannot be expected to
manage a Python install (students in a lecture hall, conference demos,
collaborators on a locked-down workstation).
