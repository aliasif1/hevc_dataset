FROM python:3.9-slim

# Acknowledgements: https://github.com/slhck/ffmpeg-quality-metrics.git
# Acknowledgements: https://johnvansickle.com/ffmpeg/

RUN apt-get update -qq -y && apt-get install -qq -y \
  wget \
  xz-utils \
  python3-pandas \
  --no-install-recommends && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget -q https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz && \
  tar --strip-components 1 -xf ffmpeg-git-amd64-static.tar.xz && \
  cp ffmpeg /usr/bin/ffmpeg && \
  cp -R model /usr/local/share/ && \
  rm ffmpeg-git-amd64-static.tar.xz

RUN pip3 install pandas
RUN pip3 install ffmpeg-progress-yield>=0.0.2
RUN pip3 install tqdm

# Install the ffmpeg_quality_metrics - https://github.com/slhck/ffmpeg-quality-metrics.git
RUN pip3 install ffmpeg_quality_metrics

# Install ffprobe
RUN pip3 install ffprobe 
RUN mv /ffprobe /usr/bin 

RUN mkdir /code
WORKDIR /code 

COPY script_docker.py ./ 

CMD [ "python3", "script_docker.py"]


