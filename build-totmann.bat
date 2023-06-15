@echo off

echo ******************************
echo * Building totmann.exe
echo ******************************

pyinstaller --onefile ^
  --clean ^
  --name totmann ^
  --noconsole ^
  --paths=.\myvenv\Lib\site-packages ^
  .\app_totmann.py 
  
del totmann.exe
copy dist\totmann.exe .
dir

echo ******************************
echo * Done building totmann.exe 
echo ******************************