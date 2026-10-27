# Quiz Game

## Build the Windows executable

From this directory, install PyInstaller and build the one-file application:

```powershell
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm my_quiz.spec
```

The executable is written to `dist\my_quiz.exe`. The build includes the quiz JSON
files and PNG logos. Quiz results are appended to `result.txt` beside the
executable.
