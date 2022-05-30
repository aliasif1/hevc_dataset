"""
Author Sonali Keshava Murthy Naik (sonali.keshavamurthy@ucalgary.ca)
This script splits a y4m file into smaller mp4 segments afterwhich it split the segments into tile dimesnions. Further it encodes the tiles and captures encoding details like time
bitrate, psnr, ssim, vmaf
"""

import os
import sys
import subprocess
import time
import json
from tilesConfig import *

class videoEncoder:
    def __init__(self, segments,rawSegmentsOutputPath,videoName,duration,dimension,videoResolution) -> None:
        self.videoName = videoName
        self.segments = segments
        self.rawSegmentsOutputPath = rawSegmentsOutputPath
        self.duration = duration
        self.dimension=dimension
        self.videoResolution = videoResolution
        

    def encode(self):
        # Create the folders where the videos will be stored
        print(f'Creating Encoding Directories for {self.videoName}')
        self.createEncoderDirectory()

        # start the encoding
        for resolution in targetResolutions:
            resolutionh=targetResolutions[resolution]
            for segment in self.segments:
                segmentName = segment.replace('.mp4','')
                #split into tiles
                inputPath = f'{self.rawSegmentsOutputPath}/segment/{segment}'
                outputPath = f'{self.rawSegmentsOutputPath}/{self.dimension}tileDim/{resolution}'
                createDirectory(outputPath)
                tilesOutputPath = f'{outputPath}/{segmentName}'
                tilew=int(int(resolution)/dimension)
                tileh=int(int(resolutionh)/dimension)
                count=0
                for x in range(dimension):
                    for y in range(dimension):
                        currTilew=x*tilew
                        currTileh=y*tileh
                        command=f'ffmpeg -y -i {inputPath} -filter_complex "scale={resolution}:{resolutionh},crop={tilew}:{tileh}:{currTilew}:{currTileh}" -c libx265  -pix_fmt yuv420p {tilesOutputPath}_tile{count}.mp4 >/dev/null 2>&1'
                        #print(command)
                        print(f'splitting {segment} into {segmentName}_tile{count}.mp4 ({dimension}*{dimension}) tile dimension at {resolution}')
                        startTime = time.time()         
                        subprocess.call(command, shell=True)
                        timeElapsedTiles = time.time() - startTime
                        #print(timeElapsedTiles)
                        tile=f'{segmentName}_tile{count}.mp4'
                        #encode the tile
                        statsArray = []
                        for crf in crfValues:
                            referenceVideoPath = f'{self.rawSegmentsOutputPath}/{dimension}tileDim/{resolution}/{tile}'
                            encodedVideoPath = f'{encodedVideoDirectoryPath}/{self.videoName}/{self.videoResolution}/{self.duration}sec/{dimension}tileDim/{resolution}/{crf}_crf/{tile}'
                            command=f'ffmpeg -y -i {referenceVideoPath}  -vcodec libx265  -preset {preset} -tune {tune} -crf {crf} -x265-params frame-threads={frameThreads}:slices={slices}:wpp={wpp}:pools={pools} -pix_fmt yuv420p {encodedVideoPath} >/dev/null 2>&1'
                            print(f'**Encoding {duration}sec {tile} at CRF: {crf}')
                            #print(command)
                            startTime = time.time()         
                            subprocess.call(command, shell=True)
                            timeElapsed = time.time() - startTime
                            transcodingStats = self.getStats(referenceVideoPath,encodedVideoPath, timeElapsed+int(timeElapsedTiles))
                            statsArray.append({crf: transcodingStats.copy()})
                            #command = f'ffmpeg -y -i {referenceVideoPath} -c:v libx265 -preset {preset} -tune {tune}  -crf {crf} -vf scale={resolution} -pix_fmt yuv420p  {encodedVideoPath} >/dev/null 2>&1'
                        self.writeDataToCsv(tile, self.duration,dimension, self.videoResolution, f'{resolution}x{resolutionh}', statsArray)
                        count=count+1

    def createEncoderDirectory(self):
        basePath = f'{encodedVideoDirectoryPath}/{self.videoName}/{self.videoResolution}/{self.duration}sec/{dimension}tileDim'
        for resolution in targetResolutions:
            for crf in crfValues:
                path = f'{basePath}/{resolution}/{crf}_crf'
                createDirectory(path) 

    def getStats(self, referenceVideoPath, encodedVideoPath, transcodingTime):
        videoStats = self.getEncodedVideoStats(encodedVideoPath)
        qualityMetrics = self.getQualityMetrics(referenceVideoPath, encodedVideoPath)
        stats = {**videoStats, **qualityMetrics, 'transcodingTime':transcodingTime}
        # print(stats)
        return(stats)

    def writeDataToCsv(self, name, duration,tileDim, sourceResolution, targetResolution, stats):
        arr = [name, duration, tileDim,sourceResolution, targetResolution]
        # print(stats)
        for crfStats in stats:
            for k, v in crfStats.items():
                arr.append(v['transcodingTime'])
                arr.append(v['bitrate'])
                arr.append(v['psnr'])
                arr.append(v['ssim'])
                arr.append(v['vmaf'])
        # print(arr)
        dataString = ','.join(str(e) for e in arr)
        appendCSV(csvPath, dataString)

    

    def getEncodedVideoStats(self,video):
        command = f"ffprobe -i {video} 2>&1"
        output = subprocess.check_output(command, shell=True)
        output = output.decode('utf-8')
        output = output.strip()
        outputArr = output.split('\n')
        durationData = [x for x in outputArr if "Duration" in x][0]
        videoData = [x for x in outputArr if "Video:" in x][0]
        duration = float([x for x in durationData.split(',') if "Duration" in x][0].split(':')[3].strip())
        fps =  float([x for x in videoData.split(',') if "fps" in x][0].strip().split(' ')[0])
        bitrate =  int([x for x in videoData.split(',') if "kb/s" in x][0].strip().split(' ')[0])
        res = [x for x in videoData.split(',') if "x" in x][1].strip().split(' ')[0]
        width = int(res.split('x')[0])
        height = int(res.split('x')[1])
        return {
            'duration': duration,
            #'fps': fps,
            'bitrate': bitrate,
            # 'width': width, 
            # 'height': height
        }        

    def getQualityMetrics(self, referenceVideoPath, encodedVideoPath):
        vmafModel = 'vmaf_v0.6.1.json'
        if (self.videoResolution == '3840x2160'):
            vmafModel = 'vmaf_4k_v0.6.1.json'

        qualities = ['psnr','ssim','vmaf']
        metrics = {}
        for quality in qualities: 
            command = f'ffmpeg_quality_metrics {encodedVideoPath} {referenceVideoPath} -m {quality} --model-path {vmafModel}'
            #print(command)
            output = subprocess.check_output(command,shell=True)
            output = output.decode('utf-8')
            output = json.loads(output)['global'][quality]['average']
            metrics[quality] = output
        return(metrics)

def removeDirectoryContents(path):
    command = f'rm -rf {path}'
    subprocess.call(command, shell=True)

def createDirectory(path):
    # check if a directory exists, if not create it
    if not os.path.exists(path):
        os.makedirs(path, mode=0o777)


def splitVideoIntoSegments(videoPath, segmentDuration,rawSegmentsOutputPath):
    command = f"ffprobe -i {videoPath} 2>&1"
    output = subprocess.check_output(command, shell=True)
    output = output.decode('utf-8')
    output = output.strip()
    outputArr = output.split('\n')
    videoData = [x for x in outputArr if "Video:" in x][0]
    fps =  float([x for x in videoData.split(',') if "fps" in x][0].strip().split(' ')[0])
    outputDirectoryPath = f'{rawSegmentsOutputPath}/segment'
    createDirectory(outputDirectoryPath)
    gop=int(fps)*int(segmentDuration)
    command = f'ffmpeg -y -i {videoPath} -c:v libx264 -preset slow -crf 22  -vf scale=426x240 -pix_fmt yuv420p -g {gop} -segment_time {segmentDuration} -reset_timestamps 1 -sc_threshold 0 -force_key_frames "expr:gte(t,n_forced*{segmentDuration})" -f segment -an {outputDirectoryPath}/{videoName}%2d.mp4 >/dev/null 2>&1'
    #command = f'ffmpeg -y -i {videoPath} -pix_fmt yuv420p -segment_time {segmentDuration} -f segment {outputDirectoryPath}/{videoName}%2d.mp4 >/dev/null 2>&1'
    print(f'splittng {videoName} into {segmentDuration} second segments')
    #print(command)
    subprocess.call(command, shell=True)
    return outputDirectoryPath    

def getDirectoryContents(path):
    contents = list(os.listdir(path))
    contents.sort()
    return contents

def checkLastSegment(directoryPath,segment, duration):
    path = f'{directoryPath}/{segment}'
    command = f'ffprobe -i {path} 2>&1 | grep Duration'
    response = subprocess.check_output(command, shell=True)
    response = response.decode("utf-8")
    responseDuration = float((response.split(',')[0])[-5:])
    if(responseDuration != duration):
        return False
    return True

def appendCSV(csvPath, data):
    with open(csvPath, 'a') as f:
        f.write(f'{data}\n')

#Driver code

# configurations
# Check that the raw segment directory exists
createDirectory(rawSegmentsDirectoryPath)

# Check that the encoded segment directory exists
createDirectory(encodedVideoDirectoryPath)

# Check that the results directory exists
createDirectory(resultsDirectoryPath)
csvPath = f'{resultsDirectoryPath}/{resultsFile}'

# Create headers for the results file
headers = ['segment', 'duration', 'tileDim', 'sourceResolution', 'targetResolution']
for crf in crfValues:
    headers.append(f'crf{crf}_tt')
    headers.append(f'crf{crf}_bitrate')
    headers.append(f'crf{crf}_psnr')
    headers.append(f'crf{crf}_ssim')
    headers.append(f'crf{crf}_vmaf')

headersString = ','.join(str(e) for e in headers)
appendCSV(csvPath, headersString)

for duration in segmentLenghts:
    for video in videos:
        videoName = video['name']
        videoPath = video['path']
        videoResolution = video['resolution']
        rawSegmentsOutputPath=f'{rawSegmentsDirectoryPath}/{videoName}/{duration}sec'
        # split the video into segments
        splitVideoIntoSegments(videoPath, duration, rawSegmentsOutputPath)
        
        segments = getDirectoryContents(f'{rawSegmentsOutputPath}/segment')
        for dimension in tileDim:
            videoObject = videoEncoder(segments,rawSegmentsOutputPath,videoName ,duration,dimension,videoResolution)
            videoObject.encode()
            
        # Remove the videoDirectory of split y4m to save space 
        removeDirectoryContents(rawSegmentsDirectoryPath)
        

