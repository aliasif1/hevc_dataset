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
from config_MPD_360_tiles_docker import *

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

def concate(target):
    for index in range(int(tileDim)*int(tileDim)):
        outputDirectoryPath = f'{tempDir}/concate_{target}_{index}.mp4'
        command = f'ffmpeg -y -f concat -safe 0 -i {tempDir}/{target}_{index}.txt -c copy {outputDirectoryPath} >/dev/null 2>&1'
        subprocess.call(command, shell=True)

def generateMPD(concatePath, MPDfilesPath ,descripter,mapCount,streamSet):
    command=f'ffmpeg -y  {concatePath} {mapCount}  -c copy -adaptation_sets "{descripter}" -f dash {MPDfilesPath}/output.mpd'# >/dev/null 2>&1'
    #print(command)
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
        tileCount=0
        descripter=f''
        mapCount=f''
        streamCount=0
        for x in range(int(tileDim)):
            for y in range(int(tileDim)):
                streamSet=f''
                for target in targetResolutions:
                    videoPath=f'{encodedVideoDirectoryPath}/{videoName}/{videoResolution}/{segmentLenghth}sec/{tileDim}tileDim/{target}/{crfValue}_crf'
                    tiles = getDirectoryContents(videoPath)
                    txtPath = f'{tempDir}/{target}_{tileCount}.txt'
                    for tile in tiles:
                        if f'_tile{tileCount}' in tile:
                            appendTXT(txtPath,f'{videoPath}/{tile}')
                    concate(target)
                    concatePath=f'{concatePath} -i {tempDir}/concate_{target}_{tileCount}.mp4'
                    mapCount=f'{mapCount} -map {streamCount}'
                    streamSet=f'{streamSet}{streamCount},'
                    streamCount=streamCount+1
                streamSet = streamSet[:-1]
                descripter=f'{descripter} id={tileCount},descriptor=<SupplementalProperty schemeIdUri=\\"urn:mpeg:dash:srd:2014\\" value=\\"0,{x},{y},1,1,{tileDim},{tileDim}\\"/>,streams={streamSet}'
                tileCount=tileCount+1
        MPDfilesPath=f'{resultsDirectoryPath}/{videoName}' 
        createDirectory(MPDfilesPath)
        generateMPD(concatePath, MPDfilesPath,descripter, mapCount,streamSet)
           
removeDirectoryContents(tempDir)
