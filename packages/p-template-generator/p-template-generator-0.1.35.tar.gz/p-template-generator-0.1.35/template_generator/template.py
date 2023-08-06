import sys
import os
import subprocess
import json
import random
from pathlib import Path
import shutil
import zipfile
import stat
from template_generator import binary

def linuxBinary(rootDir):
    binaryFile = os.path.join(rootDir, "skymedia", "TemplateProcess.out")
    if os.path.exists(binaryFile):
        return binaryFile
    return ""

def linuxEnvCheck(rootDir):
    if os.path.exists("/usr/lib/libskycore.so") == False:
        setupShell = os.path.join(rootDir, "skymedia", "setup.sh")
        if os.path.join(setupShell):
            print(f"=================== begin Initialize environment : sh {setupShell} ==================")
            try:
                cmd = subprocess.Popen(f"sh {setupShell}", stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, shell=True)
                while cmd.poll() is None:
                    print(cmd.stdout.readline().rstrip().decode('utf-8'))
            except subprocess.CalledProcessError as e:
                raise e
        
            binaryFile = os.path.join(rootDir, "skymedia", "TemplateProcess.out")
            if os.path.exists(binaryFile):
                cmd = subprocess.Popen(f"chmod 755 {binaryFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                while cmd.poll() is None:
                    print(cmd.stdout.readline().rstrip().decode('utf-8'))
            print("===================             end              ==================")

    return os.path.exists("/usr/lib/libskycore.so")

def getBinary(rootDir):
    binary = ""
    if sys.platform == "win32":
        binary = winBinary(rootDir)
    elif sys.platform == "linux":
        binary = linuxBinary(rootDir)
        if linuxEnvCheck(rootDir) == False:
            print("linux environment error")
    return binary

def winBinary(rootDir):
    binaryFile = os.path.join(rootDir, "skymedia", "win", "TemplateProcess.exe")
    if os.path.exists(binaryFile):
        return binaryFile
    return ""

def autoTemplate(videoFile, searchPath):
    rootDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        binary.updateBin(rootDir)
    else:
        rootDir = searchPath
        
    binaryPath = getBinary(rootDir)
    if len(binaryPath) <= 0:
        raise Exception("binary not found")
        
    command = f'{binaryPath} --auto {videoFile}'
    print(f"=== executeTemplate => {command}")
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while cmd.poll() is None:
        print(cmd.stdout.readline().rstrip().decode('utf-8'))
    if os.path.exists(videoFile) == False:
        raise Exception("output file not found")

def executeTemplate(inputFiles, template_path, params, output_path, searchPath):
    rootDir = ""
    if len(searchPath) <= 0 or os.path.exists(searchPath) == False:
        rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
        binary.updateBin(rootDir)
    else:
        rootDir = searchPath
        
    binaryPath = getBinary(rootDir)
    if len(binaryPath) <= 0:
        raise Exception("binary not found")

    inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{random.randint(100,99999999)}.in")
    if os.path.exists(inputArgs):
        os.remove(inputArgs)
    with open(inputArgs, 'w') as f:
        json.dump({
            "input": inputFiles,
            "template": template_path,
            "params": params,
            "output": output_path
        }, f)

    extArgs = ""
    templateName = os.path.basename(template_path)
    if "template_" in templateName or templateName == "AIGC_1":
        extArgs = "--adaptiveSize true"

    command = f'{binaryPath} --config {inputArgs} {extArgs}'
    print(f"=== executeTemplate => {command}")
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while cmd.poll() is None:
        print(cmd.stdout.readline().rstrip().decode('utf-8'))
    if os.path.exists(output_path) == False:
        raise Exception("output file not found")

def runCommand(args):
    rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    binary = getBinary(rootDir)
    if len(binary) <= 0:
        raise Exception("binary not found")
    
    command = f'{binary} --exec {args}'
    print(f"=== runCommand => {command}")
    try:
        cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while cmd.poll() is None:
            print(cmd.stdout.decode(encoding="utf8", errors="ignore"))
    except subprocess.CalledProcessError as e:
        print("====================== process error ======================")
        raise e
