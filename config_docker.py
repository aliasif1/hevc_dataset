# The mount directory has to be /app. Do not change that 

# dictionery of video name and its location 
videos = [
    {
        'name':'yacht_ride',
        'path': '/app/YachtRide_3840x2160.y4m', #inside the container
        'resolution': '3840x2160'
    }
]

# the segment length to split the video into
segmentLenghts = [1, 2]

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
crfValues = [16,18,20,22,24,26,28]


# the path inside the container where the encoded videos should be stored
encodedVideoDirectoryPath = '/app/EncodedSegments'

# the results path inside the container
resultsDirectoryPath = '/app/Results'

# the results file name
resultsFile = 'Result.csv'

# Raw Segments directory inside the container. Where the raw split segmnets will go to
rawSegmentsDirectoryPath = '/app/RawSegments'

# preset
preset = 'ultrafast'

# tune
tune = 'zerolatency'