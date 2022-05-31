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
encodedVideoDirectoryPath = '/home/ubuntu/hevc_dataset/EncodedSegments'

# the absolute results path 
resultsDirectoryPath = '/home/ubuntu/hevc_dataset/kangarooMPDFiles'


