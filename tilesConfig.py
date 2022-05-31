
# dictionery of video name and its location 
videos = [
    {
        'name':'Paris',
        'path': '/hevc/y4mvideos/video2_60_paris.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Sunset',
        'path': '/hevc/y4mvideos/video1_50_sunset.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Drone',
        'path': '/hevc/y4mvideos/video6_25_drone.y4m',
        'resolution': '3840x2160'
    },
    {
        'name':'Peaks',
        'path': '/hevc/y4mvideos/video4_50_peaks.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Venice',
        'path': '/hevc/y4mvideos/video5_25_Venice.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Perils',
        'path': '/hevc/y4mvideos/video7_30_Perils.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Pac-Man',
        'path': '/hevc/y4mvideos/video8_25_pacman.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Insight',
        'path': '/hevc/y4mvideos/video3_60_Insight.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Chariot',
        'path': '/hevc/y4mvideos/video9_24_chariot.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'RollerCoaster',
        'path': '/hevc/y4mvideos/video10_30_RollerCoaster.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Diving',
        'path': '/hevc/y4mvideos/video11_30_driving.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Kangaroo',
        'path': '/hevc/y4mvideos/video12_30_kangaroo.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'MegaCoaster',
        'path': '/hevc/y4mvideos/video13_30_megacoaster.y4m', 
        'resolution': '3840x2160'
    },
    {
        'name':'Shark',
        'path': '/hevc/y4mvideos/video14_30_shark.y4m', 
        'resolution': '3840x2160'
    }
]

# the segment length to split the video into
segmentLenghts = [1,2]

# tile dimension to split in
tileDim = [2,4] #example (2x2) , (4x4)

# the codec to consider
# valid values: avc, hevc, av1   
codec = 'av1' 

# target resolutions to consider 
targetResolutions = {
        '3840':'2160',
        '1920':'1078',
        '960':'540'
        }

# crf values to consider
# valid range [0-51] for avc and hevc
# Valid range [0-63] for av1
crfValues = [16,18,20,22,24,26,28]


# the path inside the container where the encoded videos should be stored
encodedVideoDirectoryPath = 'EncodedSegments'

# the results path inside the container
resultsDirectoryPath = 'Results'

# the results file name
resultsFile = 'ResultTiledFinal.csv'

# Raw Segments directory inside the container. Where the raw split segmnets will go to
rawSegmentsDirectoryPath = 'RawSegments'

# preset
# only used for avc and hevc 
preset = 'ultrafast'

# tune
# only used for avc and hevc
tune = 'zerolatency'

# cpu-used 
# only used for av1
# valid value range [0-8]
cpuUsed=8
