import sys
import os
import subprocess
import json
import shutil
import zipfile
from template_generator import template
from template_generator import binary

def updateRes(rootDir):
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
                return
        if root != files:
            break

def test():
    rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test")
    updateRes(rootDir)
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    binary.updateBin(binDir)
    config = {
        "input":[
            f"{rootDir}/res/1.png",
            f"{rootDir}/res/2.png",
            f"{rootDir}/res/3.png",
            f"{rootDir}/res/4.png"
            ],
        "template":f"{rootDir}/res/template",
        "params":{},
        "output":f"{rootDir}/res/out.mp4"
        }
    with open(os.path.join(rootDir, "res", "param.config"), 'w') as f:
        json.dump(config, f)

    binaryPath = template.getBinary(binDir)
    if len(binaryPath) <= 0:
        print("binary not found")
        return
        
    command = f'{binaryPath} --config {os.path.join(rootDir, "res", "param.config")}'
    print(f"test template command => {command}")
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while cmd.poll() is None:
        print(cmd.stdout.readline().rstrip().decode('utf-8'))
