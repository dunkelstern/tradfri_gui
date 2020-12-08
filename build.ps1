$env:PATH="$env:PATH;C:\Windows\System32\downlevel;C:\Program Files (x86)\NSIS"
pyinstaller --name="TradfriGUI" --windowed --onedir --noupx -y src\main.py
Copy-Item "bin\*.dll" ".\dist\TradfriGUI\"
Copy-Item "bin\*.exe" ".\dist\TradfriGUI\"
New-Item -Path ".\dist\TradfriGUI\" -Name "pytradfri" -ItemType "directory" -Force
Copy-Item "$env:VIRTUAL_ENV\Lib\site-packages\pytradfri\VERSION" ".\dist\TradfriGUI\pytradfri\"
Copy-Item -Recurse "icons" ".\dist\TradfriGUI\"
makensis /X"SetCompressor /FINAL lzma" installer.nsis
