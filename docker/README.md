docker pull --platform linux/arm64 taoluo/orpheus:latest

docker run -it --rm  -v /tmp/youtube:/data --entrypoint bash  taoluo/orpheus

docker run  -v /tmp/youtube:/data  taoluo/orpheus:whisper Uam5vk7fnkY