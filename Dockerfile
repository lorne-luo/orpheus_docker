FROM python:3.9.18-slim-bullseye as spleeter
RUN apt-get update
RUN apt install -y ffmpeg opencc

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install spleeter
RUN pip3 install yt-dlp

ADD https://github.com/deezer/spleeter/releases/download/v1.4.0/2stems.tar.gz /tmp
# RUN tar -zxf  /data/pretrained_models/2stems.tar.gz -C /data/pretrained_models/2stems
ADD audio_example.mp3 /tmp

ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["/y2ok.sh"]


FROM python:3.9.18-slim-bullseye as whisper-base
RUN apt-get update
RUN apt install -y ffmpeg opencc

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install openai-whisper torch==1.10.1
RUN pip3 install soundfile librosa srt yt-dlp
ADD audio_example.mp3 /tmp

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
RUN pip3 install soundfile librosa srt yt-dlp
# add medium model
ADD https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt /root/.cache/whisper/medium.pt
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["/y2ok.sh"]


FROM taoluo/orpheus:spleeter as spleeter-whisper-large

RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install openai-whisper torch==1.10.1
RUN pip3 install soundfile librosa srt yt-dlp
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
ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["/v2ok.sh"]


FROM taoluo/orpheus:spleeter as y2ok
ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ENTRYPOINT ["/y2ok.sh"]


FROM taoluo/orpheus:allinone as whisper
ADD v2ok.sh /v2ok.sh
RUN chmod +x /v2ok.sh
ADD y2ok.sh /y2ok.sh
RUN chmod +x /y2ok.sh
ADD whisper.sh /whisper.sh
RUN chmod +x /whisper.sh
ENTRYPOINT ["/y2ok.sh"]
