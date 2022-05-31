# dictionery of video name and its location 
videos = [
    {
        'name':'yacht_ride',
        'path': '/home/asif/Documents/VideosDataset/YachtRide_3840x2160_120fps_420_8bit_YUV_Y4M/YachtRide_3840x2160.y4m',
        'resolution': '3840x2160'
    },
    # {
    #     'name':'river_bank',
    #     'path':'/home/asif/Documents/VideosDataset/RiverBank_3840x2160_50fps_420_8bit_YUV_RAW/RiverBank_3840x2160_50fps_8bit.y4m',
    #     'resolution': '3840x2160'
    # },
]

# the segment length to split the video into
segmentLenghts = [1]

# the codec to consider
# valid values: avc, hevc, av1   
codec = 'av1' 

# target resolutions to consider 
targetResolutions = [
    # '3840x2160',
    # '1920x1080',
    # '1280x720',
    # '1024x576',
    '640x360'
]

# crf values to consider 
# valid range [0-51] for avc and hevc 
# Valid range [0-63] for av1
crfValues = [40]

# the absolute path where the encoded videos should be stored
encodedVideoDirectoryPath = '/home/VideosDataset/EncodedSegments3'

# the absolute results path 
resultsDirectoryPath = '/home/VideosDataset/Results'

# the results file name
resultsFile = 'Result.csv'

# Raw Segments directory. Wheret the raw split segmnets will go to
rawSegmentsDirectoryPath = '/home/VideosDataset/RawSegments'

# preset
# only used for avc and hevc 
preset = 'ultrafast'

# tune
# only used for avc and hevc 
tune = 'zerolatency'

# cpu-used 
# only used for av1
# valid value range [0-8]
cpuUsed = 8