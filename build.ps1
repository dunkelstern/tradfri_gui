$env:PATH="$env:PATH;C:\Windows\System32\downlevel;C:\Program Files (x86)\NSIS"
pyinstaller --name="TradfriGUI" --windowed --onedir --noupx -y src\main.py
Copy-Item "bin\*.dll" ".\dist\TradfriGUI\"
Copy-Item "bin\*.exe" ".\dist\TradfriGUI\"
Copy-Item -Recurse "icons" ".\dist\TradfriGUI\"
