echo linijka
@REM .venv\Scripts\activate.bat
echo linijka1
pyinstaller --paths .\.venv\Lib\site-packages --hidden-import "pygame.freetype" --noconsole main.py -y
echo linijka2
xcopy .\assets .\dist\main\assets /s /e /h /I