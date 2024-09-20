import PyInstaller.__main__
import shutil
import os

try:
    shutil.rmtree(".\\build")
except:
    pass
try:
    shutil.rmtree(".\\dist")
except:
    pass

try:
    os.remove("asmcli.spec")
except:
    pass

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--paths=.\\venv\\Lib\\site-packages',
    '--name=asmcli'
])