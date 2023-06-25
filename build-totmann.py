import os
import datetime
import shutil
import PyInstaller.__main__ as pyi
import win32com.client

shutil.rmtree("dist", ignore_errors=True)

pyi.run([
    "app_totmann.py",
    "--name=totmann",
    "--icon=./tm_32.ico",
    "--onefile",
    "--clean",
    "--noconsole",
    "--paths=./.venv/Lib/site-packages",])

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
targetDir = "dist/"+timestamp+"/"
os.makedirs(targetDir, exist_ok=True)
os.rename("dist/totmann.exe", targetDir+"totmann.exe")

path = os.path.join(os.environ["USERPROFILE"], "Desktop", 'Totmann.lnk')
target = os.path.abspath(targetDir+"totmann.exe")
# icon = r'C:\path\to\icon\resource.ico'  # not needed, but nice

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut(path)
shortcut.Targetpath = target
# shortcut.IconLocation = icon
shortcut.WindowStyle = 1  # 7 - Minimized, 3 - Maximized, 1 - Normal
shortcut.save()

print("Done")
