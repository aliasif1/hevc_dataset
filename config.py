# dictionery of video name and its location 
videos = [
    {
        'name':'vid_name',
        'path': 'vid_path',
        'resolution': '3840x2160'
    },
]

# the segment length to split the video into
segmentLenghts = [1,2]

# the codecs to consider  
codecs = ['hevc']

# target resolutions to consider 
targetResolutions = [
    '3840x2160',
    '1920x1080',
    '1280x720',
    '1024x576',
    '640x360'
]

# crf values to consider 
crfValues = [16,22,28]

# the absolute path where the encoded videos should be stored
encodedVideoDirectoryPath = 'path'

# the absolute results path 
resultsDirectoryPath = 'path'

# the results file name
resultsFile = 'result.csv'

# Raw Segments directory. Wheret the raw split segmnets will go to
rawSegmentsDirectoryPath = 'path'

# preset
preset = 'ultrafast'

# tune
tune = 'zerolatency'