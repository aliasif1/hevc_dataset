# dictionery of video name and its location 
videos = [
    {
        'name':'yacht_ride',
        'path': '/home/ubuntu/Documents/VideosDataset/YachtRide_3840x2160_120fps_420_8bit_YUV_Y4M/YachtRide_3840x2160.y4m',
        'resolution': '3840x2160'
    },
    {
        'name':'river_bank',
        'path':'/home/ubuntu/Documents/VideosDataset/RiverBank_3840x2160_50fps_420_8bit_YUV_RAW/RiverBank_3840x2160_50fps_8bit.y4m',
        'resolution': '3840x2160'
    },
]

# the segment length to split the video into
segmentLenghts = [1, 2]

# the codec to consider
# valid values: avc, hevc   
codec = 'hevc' 

# target resolutions to consider 
targetResolutions = [
    '3840x2160',
    '1920x1080',
    '1280x720',
    '1024x576',
    '640x360'
]

# crf values to consider 
crfValues = [16,18,20,22,24,26,28]


# the absolute path where the encoded videos should be stored
encodedVideoDirectoryPath = '/home/ubuntu/Documents/VideosDataset/EncodedSegments3'

# the absolute results path 
resultsDirectoryPath = '/home/ubuntu/Documents/VideosDataset/Results'

# the results file name
resultsFile = 'Result.csv'

# Raw Segments directory. Wheret the raw split segmnets will go to
rawSegmentsDirectoryPath = '/home/ubuntu/Documents/VideosDataset/RawSegments'

# preset
preset = 'ultrafast'

# tune
tune = 'zerolatency'