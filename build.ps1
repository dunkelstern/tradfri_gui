$env:PATH="$env:PATH;C:\Windows\System32\downlevel;C:\Program Files (x86)\NSIS"
pyinstaller --name="TradfriGUI" --windowed --onedir --noupx -y src\main.py
copy "bin\*.dll" ".\dist\TradfriGUI\"
copy "bin\*.exe" ".\dist\TradfriGUI\"
