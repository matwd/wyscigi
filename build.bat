@REM .venv\Scripts\activate.bat
echo plik bat użyty
pyinstaller --paths .\.venv\Lib\site-packages  --hidden-import "pygame.freetype" --noconsole main.py -y --icon=assets/logo.ico
echo folder dist utworzony
xcopy .\assets .\dist\main\assets /s /e /h /I
echo dodanie folderu assets do dist/main