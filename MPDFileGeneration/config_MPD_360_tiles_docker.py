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
tileDim = 4

targetResolutions = {
        '3840':'2160',
        '960':'540'
        }

# crf value to consider 
crfValue = 28

# the absolute path where the encoded videos are stored
encodedVideoDirectoryPath = '/app/hevc_dataset/EncodedSegments'

# the absolute results path 
resultsDirectoryPath = '/app/hevc_dataset/kangarooMPDFiles'


