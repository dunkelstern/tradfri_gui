# Tradfri GUI

Simple Qt based Tradfri GUI implemented in Python.

## Requirements

### Running

- Python >=3.6
- PySide2 ~=5.14
- [pytradfri](https://github.com/ggravlingen/pytradfri) master checkout

### Building

**Windows:**

- `pywin32`
- `pywin32-ctypes`
- NSIS
- `libcoap.dll`/`coap-client.exe` (supplied in the `bin` dir, you may rebuild them yourself if you want)

**All Systems:**

- Poetry
- `pyinstaller`

## Building

### Windows

1. Make sure you have NSIS installed.
2. Make sure you have a Version of Python>=3.6 installed (Not the Microsoft Store Version!)
3. Install `poetry`: `pip install poetry`
4. Create a virtualenv: `poetry install --dev`
5. Run the build script: `./build.ps1`

The build script will create an installation in `dist/TradfriGUI` and an installer file in `dist`

### Linux

TODO

### Mac OS

TODO
