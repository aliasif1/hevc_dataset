# The mount directory has to be /app. Do not change that 

# dictionery of video name and its input resolution 
videos = [
    {
        'name':'Kangaroo',
        'resolution': '3840x2160'
    }
]

# the segment length to stream
segmentLenghth = 1

targetResolutions = [
    '3840x2160',
    '1920x1078',
    '960x540'
]

# crf value to consider 
crfValue = 28

# the path inside the container where the encoded videos should be stored
encodedVideoDirectoryPath = '/app/hevc_dataset/EncodedSegments'

# the results path inside the container
resultsDirectoryPath = '/app/hevc_dataset/jockeyMPDfiles'


