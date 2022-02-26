# Dataset Link
The dataset is availabe [here](https://drive.google.com/drive/folders/1PHBWy-Gq66OZd73e3L_SJMP9gwgupM24?usp=sharing)

# HEVC Dataset
This repository contains the HEVC dataset comprising of 1 second and 2 second long segments (suitable for low latency applications) as well as the tool to generate HEVC encoded segments using CRF as the rate control mode. 

## Raw Scripts
Add Implementation details of the raw script

## Docker 
Add Implementation details for Docker

## OurDataset
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
