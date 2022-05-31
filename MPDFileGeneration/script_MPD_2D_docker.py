"""
Author Sonali Keshava Murthy Naik (sonalik.4574@gmail.com))
This script takes segments of a original video file and generates MPD files.
"""

import os
import sys
import subprocess
import time
import json
sys.path.insert(0, '/app')
from config_MPD_2D_docker import *

def removeDirectoryContents(path):
    command = f'rm -rf {path}'
    subprocess.call(command, shell=True)

def getDirectoryContents(path):
    contents = list(os.listdir(path))
    contents.sort()
    return contents

def createDirectory(path):
    # check if a directory exists, if not create it
    command = f'mkdir {path}'
    if not os.path.exists(path):
        subprocess.call(command, shell=True)

def appendTXT(path, data):
    with open(path, 'a') as f:
        f.write(f"file '{data}'\n")

def concate(txtPath,target):
    outputDirectoryPath = f'{tempDir}/concate_{target}.mp4'
    command = f'ffmpeg -y -f concat -safe 0 -i {txtPath} -c copy {outputDirectoryPath} >/dev/null 2>&1'
    subprocess.call(command, shell=True)
    return outputDirectoryPath

def generateMPD(concatePath, MPDfilesPath ,mapCount,streamSet):
    command = f"ffmpeg -y -re {concatePath} {mapCount}  -c copy -use_timeline 0 -use_template 1 -f dash -adaptation_sets 'id=0,streams={streamSet}' -seg_duration {segmentLenghth} -index_correction 1 -ldash 1 {MPDfilesPath}/output.mpd >/dev/null 2>&1"
    print("Generating MPD files")
    subprocess.call(command, shell=True)

createDirectory(resultsDirectoryPath)
tempDir = f'tmp'
createDirectory(tempDir)

for video in videos:
        videoName = video['name']
        videoResolution = video['resolution']
        MPDPath = f'{resultsDirectoryPath}/{videoName}.mpd'
        concatePath=f''
        streamSet=f''
        count=0
        mapCount=f''
        for target in targetResolutions:
            videoPath=f'{encodedVideoDirectoryPath}/{videoName}/{videoResolution}/{segmentLenghth}sec/{target}/{crfValue}_crf'
            segments = getDirectoryContents(videoPath)
            txtPath = f'{tempDir}/{target}.txt'
            for segment in segments:
                appendTXT(txtPath,f'{videoPath}/{segment}')
            concateFile=concate(txtPath,target)
            concatePath=f'{concatePath} -i {concateFile}'
            mapCount=f'{mapCount} -map {count}'
            streamSet=f'{streamSet},{count}'
            count=count+1
        streamSet = streamSet[1:]
        MPDfilesPath=f'{resultsDirectoryPath}/{videoName}' 
        createDirectory(MPDfilesPath)
        generateMPD(concatePath, MPDfilesPath, mapCount,streamSet)
            
removeDirectoryContents(tempDir)
