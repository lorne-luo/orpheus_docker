FROM python:3.9.18-slim-bullseye as spleeter
RUN apt-get update
RUN apt install -y ffmpeg opencc gcc vim libcairo2 libcairo2-dev pkg-config python3-dev libgirepository1.0-dev

RUN pip3 install --no-cache-dir --upgrade pip yt-dlp pyonfx
RUN pip3 install spleeter numba==0.55.2 numpy==1.22.4

ADD https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz /root
RUN mkdir -p /root/2stems/
RUN tar vxf /root/2stems.tar.gz -C /root/2stems
ENV MODEL_PATH=/root
ADD audio_example.mp3 /root

ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["/y2ok.sh"]


FROM python:3.9.18-slim-bullseye as whisper-base
RUN apt-get update
RUN apt install -y ffmpeg opencc gcc vim libcairo2 libcairo2-dev pkg-config python3-dev libgirepository1.0-dev

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install openai-whisper torch==1.10.1
RUN pip3 install soundfile librosa srt yt-dlp pyonfx
ADD audio_example.mp3 /root

ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["whisper"]


FROM taoluo/orpheus:whisper-base as whisper-medium
# add medium model
ADD https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt /root/.cache/whisper/medium.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["whisper"]


FROM taoluo/orpheus:whisper-base as whisper-large
# https://github.com/openai/whisper/blob/main/whisper/__init__.py
# add large model
ADD https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt /root/.cache/whisper/large-v2.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["whisper"]


FROM taoluo/orpheus:whisper-medium as whisper-all
# add medium model
ADD https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt /root/.cache/whisper/medium.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["whisper"]


FROM taoluo/orpheus:spleeter as spleeter-whisper-medium

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install openai-whisper torch==1.10.1
RUN pip3 install soundfile librosa srt yt-dlp pyonfx
# add medium model
ADD https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt /root/.cache/whisper/medium.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["/y2ok.sh"]


FROM taoluo/orpheus:spleeter as spleeter-whisper-large

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install openai-whisper torch==1.10.1
RUN pip3 install soundfile librosa srt yt-dlp pyonfx
# add large model
ADD https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt /root/.cache/whisper/large-v2.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["/y2ok.sh"]



FROM taoluo/orpheus:spleeter-whisper-medium as allinone
# add large model
ADD https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt /root/.cache/whisper/large-v2.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["/y2ok.sh"]


FROM taoluo/orpheus:spleeter as v2ok
RUN pip3 install pyonfx
ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["/v2ok.sh"]


FROM taoluo/orpheus:spleeter as y2ok
RUN pip3 install pyonfx
ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["/y2ok.sh"]


FROM taoluo/orpheus:allinone as youtube
RUN echo 'alias ll="ls -lah"' >> /root/.bashrc
RUN apt install -y gcc libcairo2 libcairo2-dev pkg-config python3-dev libgirepository1.0-dev
RUN pip3 install pyonfx

ADD srt2ass.py /srt2ass.py
ADD subtitle_effects.py /subtitle_effects.py

ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["/y2ok.sh"]

FROM python:3.9.18-slim-bullseye as jax-base-amd64
RUN echo 'alias ll="ls -lah"' >> /root/.bashrc
RUN apt-get update
RUN apt install -y ffmpeg opencc vim

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install jaxlib==0.4.6 jax==0.4.6
RUN pip3 install click cached-property

FROM python:3.9.18-slim-bullseye as jax-base-arm64
RUN echo 'alias ll="ls -lah"' >> /root/.bashrc
RUN apt-get update
RUN apt install -y ffmpeg opencc vim git g++ python python3-dev libcairo2 libcairo2-dev pkg-config libgirepository1.0-dev

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip install numpy wheel build soundfile librosa srt yt-dlp pyonfx click cached-property

RUN git clone https://github.com/google/jax
RUN cd jax
RUN git checkout jax-v0.4.5

RUN python build/build.py
RUN pip install dist/*.whl
# installs jax
RUN pip install -e .


FROM python:3.9.18-slim-bullseye as faster-whisper-base
RUN echo 'alias ll="ls -lah"' >> /root/.bashrc
ADD audio_example.mp3 /root
RUN apt-get update
RUN apt install -y ffmpeg opencc gcc vim libcairo2 libcairo2-dev pkg-config python3-dev libgirepository1.0-dev

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install soundfile librosa srt yt-dlp pyonfx click
RUN pip3 install faster-whisper

ADD whisper_faster.py /whisper_faster.py
ENTRYPOINT ["python3", "/whisper_faster.py"]


FROM taoluo/orpheus:faster-whisper-base as faster-whisper-medium

ADD whisper_faster.py /whisper_faster.py
RUN python /whisper_faster.py /root/audio_example.mp3 -l en -m medium
ENTRYPOINT ["python3", "/whisper_faster.py"]


FROM taoluo/orpheus:faster-whisper-base as faster-whisper-large

ADD whisper_faster.py /whisper_faster.py
RUN python /whisper_faster.py /root/audio_example.mp3 -l en -m large
ENTRYPOINT ["python3", "/whisper_faster.py"]


FROM taoluo/orpheus:whisper-jax as spleeter-whisper-jax
RUN apt-get update
RUN apt install -y ffmpeg opencc gcc vim libcairo2 libcairo2-dev pkg-config python3-dev libgirepository1.0-dev
RUN pip3 install spleeter numba==0.55.2 numpy==1.22.4
RUN pip3 install soundfile librosa srt yt-dlp pyonfx

ADD https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz /root
RUN mkdir -p /root/2stems/
RUN tar vxf /root/2stems.tar.gz -C /root/2stems
ENV MODEL_PATH=/root
ADD audio_example.mp3 /root

ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ADD whisper-jax.py /whisper-jax.py
ENTRYPOINT ["python3", "/whisper-jax.py"]

FROM python:3.9.18-slim-bullseye as jax-base-arm64
RUN echo 'alias ll="ls -lah"' >> /root/.bashrc
ADD audio_example.mp3 /root
RUN apt-get update
RUN apt install -y ffmpeg opencc vim git g++ python python3-dev libcairo2 libcairo2-dev pkg-config libgirepository1.0-dev

RUN pip install --upgrade pip click
RUN pip install --upgrade "jax[cpu]" torch click
RUN pip install git+https://github.com/sanchit-gandhi/whisper-jax.git

ADD whisper-jax.py /whisper-jax.py
ENTRYPOINT ["python3", "/whisper-jax.py"]

FROM taoluo/orpheus:jax-base-arm64 as whisper-jax
RUN echo 'alias ll="ls -lah"' >> /root/.bashrc
ADD audio_example.mp3 /root
RUN apt-get update
RUN apt install -y ffmpeg opencc vim git g++ python python3-dev libcairo2 libcairo2-dev pkg-config libgirepository1.0-dev

RUN pip install --upgrade pip click
RUN pip install git+https://github.com/sanchit-gandhi/whisper-jax.git

ADD whisper-jax.py /whisper-jax.py
ENTRYPOINT ["python3", "/whisper-jax.py"]