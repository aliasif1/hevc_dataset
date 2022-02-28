# Dataset Link
The dataset is availabe [here](https://drive.google.com/drive/folders/1PHBWy-Gq66OZd73e3L_SJMP9gwgupM24?usp=sharing)

# HEVC Dataset
This repository contains the HEVC dataset comprising of 1 second and 2 second long segments (suitable for low latency applications) as well as the tool to generate HEVC encoded segments using CRF as the rate control mode. 

## Requirement
- Python (3.6 or higher)
- FFmpeg 
- FFmpeg Quality Metrics (https://github.com/slhck/ffmpeg-quality-metrics.git)
- SITI (Spatial Information / Temporal Information) (https://github.com/slhck/siti.git)

## Raw Scripts
- `script.py` (Main Script)
- `config.py` (Configuration)

## Usage
- configuration File (`config.py`) - The Configuration file contains the transcoding parameters. Please update the paths and the parameters in the config file before executing the script. 
    ```
    # List of Video Dictionery 
    # Each Dictionery is a y4m Video which needs to be segmented and converted to HEVC 
    videos = [
        {
            'name':'twilight3', # What name the segments should be.
            'path': '/home/ubuntu/Documents/VideosDataset/Twilight_3840x2160_50fps_420_8bit_YUV_RAW/Twilight_3840x2160_50fps_8bit.y4m', # Absolute path of the video file
            'resolution': '3840x2160' # Resolution of the video
        },
    ]

    # the segment lengths to split the video into
    segmentLenghts = [1, 2]

    # the codecs to consider  
    codecs = ['hevc']

    # target resolutions to transcode the segments to 
    targetResolutions = [
        '3840x2160',
        '1920x1080',
        '1280x720',
        '1024x576',
        '640x360'
    ]

    # the absolute path where the encoded videos should be stored
    # Change according to your paths
    encodedVideoDirectoryPath = '/home/ubuntu/Documents/VideosDataset/EncodedSegments'

    # the absolute results path 
    # Change according to your paths
    resultsDirectoryPath = '/home/ubuntu/Documents/VideosDataset/Results'

    # the results file name
    resultsFile = 'result.csv'

    # Raw Segments directory path 
    # Raw directory segments is where the raw splitted segmenst will go to. This is cleaned after the encoding completes
    # Change according to your paths
    rawSegmentsDirectoryPath = '/home/ubuntu/Documents/VideosDataset/RawSegments'

    # crf values to consider 
    # valid value: 1 to 51 
    crfValues = [16,18,20,22,24,26,28]

    # the preset to use
    # valid values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
    preset = 'ultrafast'

    # the tune to use
    # valid values: psnr, ssim, grain, fastdecode, zerolatency, animation
    tune = 'zerolatency'
    ```
- Run the script (`script.py`)
    ```
    python3 script.py
    ```
- The Resultant segments will be stored in the `encodedVideoDirectoryPath` and resultant CSV file in `resultsDirectoryPath`

# Docker 
## Usage
- build the docker image
    ```
    docker image build -t myimg .
    ```
- or Download the image from dockerhub 
    ```
    docker image pull "Coming Soon"
    ```
- configuration File (`config_docker.py`) - The Configuration file contains the transcoding parameters. Please update the paths and the parameters in the config file before executing the script. NOTE: The mount directory inside the container has to be /app. do not change that 
    ```
    # List of Video Dictionery 
    # Each Dictionery is a y4m Video which needs to be segmented and converted to HEVC 
    videos = [
        {
            'name':'twilight3', # What name the segments should be.
            'path': '/app/Twilight_3840x2160_50fps_420_8bit_YUV_RAW/ # the mount path on the container has to be /app. Twilight_3840x2160_50fps_8bit.y4m', # path of the video file inside the container
            'resolution': '3840x2160' # Resolution of the video
        },
    ]

    # the segment lengths to split the video into
    segmentLenghts = [1, 2]

    # the codecs to consider  
    codecs = ['hevc']

    # target resolutions to transcode the segments to 
    targetResolutions = [
        '3840x2160',
        '1920x1080',
        '1280x720',
        '1024x576',
        '640x360'
    ]

    # Path inside the container where the encoded videos should be stored
    encodedVideoDirectoryPath = '/app/EncodedSegments'

    # Results path inside the container
    # Change according to your paths
    resultsDirectoryPath = '/app/Results'

    # the results file name
    resultsFile = 'result.csv'

    # Raw Segments directory path inside the container
    # Raw directory segments is where the raw splitted segmenst will go to. This is cleaned after the encoding completes
    rawSegmentsDirectoryPath = '/app/RawSegments'

    # crf values to consider 
    # valid value: 1 to 51 
    crfValues = [16,18,20,22,24,26,28]

    # the preset to use
    # valid values: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
    preset = 'ultrafast'

    # the tune to use
    # valid values: psnr, ssim, grain, fastdecode, zerolatency, animation
    tune = 'zerolatency'
    ```
- Create a mount directory (say /mount) and copy the "config_docker.py" file and all the y4m video files which needs to be transcoded to to mount directory.

- Run the script (`script_docker.py`) from a container 
    ```
    docker container run --rm --mount type=bind,source=/mount,target=/app myimg
    ```
- The Resultant segments will be stored in the `encodedVideoDirectoryPath` and resultant CSV file in `resultsDirectoryPath` inside the mount folder 


# OurDataset
For generating our dataset we used 11 videos from the UVG dataset. The videos selected are
|     Video    |    Creator   | Resolution | FPS | Bitrate (kbps) |   Codec   | Duration (Seconds) | # 1 Second  Segments  | # 2 Second  Segments  |
|:------------:|:------------:|:----------:|:---:|:--------------:|:---------:|:------------------:|:---------------------:|:---------------------:|
|    Jockey    | UVG Dataset  |  3840x2160 |  30 |     2985985    | YUV 4:2:0 |         20         |           20          |           10          |
| Ready Set Go | UVG Dataset  |  3840x2160 |  30 |     2985985    | YUV 4:2:0 |         20         |           20          |           10          |
|   Honey Bee  | UVG Dataset  |  3840x2160 |  30 |     2985985    | YUV 4:2:0 |         20         |           20          |           10          |
|  Bosphorous  | UVG Dataset  |  3840x2160 |  30 |     2985985    | YUV 4:2:0 |         20         |           20          |           10          |
|  Yacht Ride  | UVG Dataset  |  3840x2160 |  30 |     2985985    | YUV 4:2:0 |         20         |           20          |           10          |
|  Race Night  | UVG Dataset  |  3840x2160 |  50 |     4976642    | YUV 4:2:0 |         12         |           12          |           6           |
|   Twilight   | UVG Dataset  |  3840x2160 |  50 |     4976642    | YUV 4:2:0 |         12         |           12          |           6           |
|  City Alley  | UVG Dataset  |  3840x2160 |  50 |     4976642    | YUV 4:2:0 |         12         |           12          |           6           |
|  Flower Kids | UVG Dataset  |  3840x2160 |  50 |     4976642    | YUV 4:2:0 |         12         |           12          |           6           |
| Flower Focus | UVG Dataset  |  3840x2160 |  50 |     4976642    | YUV 4:2:0 |         12         |           12          |           6           |
| River Bank   | UVG Dataset  |  3840x2160 |  50 |     4976642    | YUV 4:2:0 |         12         |           12          |           6           |



## Acknowledgements
- FFmpeg Quality Metrics (https://github.com/slhck/ffmpeg-quality-metrics.git)
- SITI (Spatial Information / Temporal Information) (https://github.com/slhck/siti.git)
