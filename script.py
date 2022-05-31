"""
Author Asif ali Mehmuda (asif.mehmuda9@gmail.com)
This script splits a y4m file into smaller y4m segments and encodes the segments and captures encoding details like time
bitrate, psnr, ssim, vmaf
"""

import code
import os
from config import *
import subprocess
import time
import json

class videoEncoder:
    def __init__(self, videoName,segments,segmentDirectoryPath,duration,videoResolution) -> None:
        self.videoName = videoName
        self.segments = segments
        self.segmentDirectoryPath = segmentDirectoryPath
        self.duration = duration
        self.videoResolution = videoResolution
        

    def encode(self):
        # Create the folders where the videos will be stored
        print(f'Creating Encoding Directories for {self.videoName}')
        self.createEncoderDirectory()

        # start the encoding
        for resolution in targetResolutions:
            for segment in self.segments:
                statsArray = []
                encodedSegmentName = segment.replace('y4m','mp4')
                for crf in crfValues:
                    referenceVideoPath = f'{self.segmentDirectoryPath}/{segment}'
                    encodedVideoPath = f'{encodedVideoDirectoryPath}/{self.videoName}/{self.videoResolution}/{self.duration}sec/{resolution}/{crf}_crf/{encodedSegmentName}'
                    print(f'**Encoding ({codec}) {duration}sec {segment} -> {encodedSegmentName} at {resolution} with CRF {crf}')
                    command = ''
                    if codec in ['avc', 'hevc']:
                        command = f'ffmpeg -i {referenceVideoPath} -c:v {CODECLIBRARY} -preset {preset} -tune {tune}  -crf {crf} -vf scale={resolution} -pix_fmt yuv420p  {encodedVideoPath} >/dev/null 2>&1'
                    elif codec == 'av1':
                        command = f'ffmpeg -i {referenceVideoPath} -c:v {CODECLIBRARY} -crf {crf} -b:v 0 -vf scale={resolution} -pix_fmt yuv420p -cpu-used {cpuUsed} {encodedVideoPath} >/dev/null 2>&1'                
                    startTime = time.time()         
                    subprocess.call(command, shell=True)
                    timeElapsed = time.time() - startTime
                    transcodingStats = self.getStats(referenceVideoPath, encodedVideoPath, timeElapsed)
                    fps = transcodingStats['fps']
                    statsArray.append({crf: transcodingStats.copy()})
                self.writeDataToCsv(segment, self.duration, fps, self.videoResolution, resolution, statsArray)

    def createEncoderDirectory(self):
        basePath = f'{encodedVideoDirectoryPath}/{self.videoName}/{self.videoResolution}/{self.duration}sec'
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

    def writeDataToCsv(self, name, duration, fps, sourceResolution, targetResolution, stats):
        arr = [name, duration, fps, sourceResolution, targetResolution]
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
            'fps': fps,
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
            output = subprocess.check_output(command,shell=True)
            output = output.decode('utf-8')
            output = json.loads(output)['global'][quality]['average']
            metrics[quality] = output
        return(metrics)

def removeDirectoryContents(path):
    command = f'rm -rf {path}/*'
    subprocess.call(command, shell=True)

def createDirectory(path):
    # check if a directory exists, if not create it
    if not os.path.exists(path):
        os.makedirs(path)

def splitVideoIntoSegments(videoName, videoPath, videoResolution,segmentDuration,rawSegmentDirectoryPath):
    outputDirectoryPath = f'{rawSegmentDirectoryPath}/{videoName}/{videoResolution}/{segmentDuration}sec'
    createDirectory(outputDirectoryPath)
    command = f'ffmpeg -i {videoPath} -f segment -segment_time {segmentDuration} -pix_fmt yuv420p {outputDirectoryPath}/{videoName}%2d.y4m >/dev/null 2>&1'
    print(f'splittng {videoName} into {segmentDuration} second segments')
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

# The ffmpeg Library/codec to use
CODECLIBRARY = None
if codec == 'hevc':
    CODECLIBRARY = 'libx265'
elif codec == 'avc':
    CODECLIBRARY = 'libx264'
elif codec == 'av1':
    CODECLIBRARY = 'libaom-av1'

# configurations
# Check that the raw segment directory exists
createDirectory(rawSegmentsDirectoryPath)

# Check that the encoded segment directory exists
createDirectory(encodedVideoDirectoryPath)

# Check that the results directory exists
createDirectory(resultsDirectoryPath)
csvPath = f'{resultsDirectoryPath}/{resultsFile}'

# Create headers for the results file
headers = ['segment', 'duration', 'fps', 'sourceResolution', 'targetResolution']
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
        # split the video into segments 
        segmentDirectoryPath = splitVideoIntoSegments(videoName, videoPath, videoResolution, duration, rawSegmentsDirectoryPath)
        segments = getDirectoryContents(segmentDirectoryPath)
        # check that the last segment has valid duration i.e. its not short
        isLastSegmentValid = checkLastSegment(segmentDirectoryPath, segments[-1], duration)
        if not isLastSegmentValid:
            segments = segments[:-1] # Exclude the last segment
        segments = segments[0:1] # comment later 
        videoObject = videoEncoder(videoName,segments,segmentDirectoryPath,duration,videoResolution)
        videoObject.encode()

        # Remove the videoDirectory of split y4m to save space 
        removeDirectoryContents(rawSegmentsDirectoryPath)