# PC Doctor v1.0

A beginner-friendly Windows diagnostic helper made with Python and Tkinter.

## Features
- System Information
- Disk Space
- Network Test
- Windows Information
- Running Processes
- Startup Apps
- Generate a PC report
- About screen

## Run

1. Install Python 3.11+.
2. Open Command Prompt in this folder.
3. Install the dependency:

```text
python -m pip install -r requirements.txt
```

4. Start the program:

```text
python main.py
```

## Notes
The program is designed as a read-only diagnostic helper. It does not automatically delete files, modify the registry, or change Windows settings.

## Optional EXE
You can later package it with PyInstaller:

```text
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name PCDoctor main.py
```

The EXE will appear inside the `dist` folder.
