#!/bin/bash
# Enable strict mode (halt on error and unset variable)
set -euo pipefail

START=$SECONDS
OUTPUT="${2:-output}"
INPUT="${1}"

if [ -z "${2:-}" ]; then
  OUTPUT="/data/output.mp4"
else
  if [[ "$2" != *.* ]]; then
    OUTPUT="/data/${2}.mp4"
  else
    OUTPUT="${2}"
  fi
fi

FOLDER=$(dirname "$OUTPUT")
AUDIO="$FOLDER/audio.wav"
VOCALS="$FOLDER/audio/vocals.wav"
SUBTITLE="$FOLDER/audio/vocals.srt"
SUBTITLE_VIDEO="$FOLDER/subtitle.mp4"
echo "INPUT=$INPUT"
echo "OUTPUT=$OUTPUT"
echo "FOLDER=$FOLDER"
echo "AUDIO=$AUDIO"
echo "VOCALS=$VOCALS"
echo "SUBTITLE=$SUBTITLE"
echo "SUBTITLE_VIDEO=$SUBTITLE_VIDEO"

if [ -f "$INPUT" ]; then
  echo "$INPUT exists."
#  cp $1 $INPUT
else
  echo "Input file $INPUT not exists"
  exit 1
fi

cd "$FOLDER"
echo "Split video and audio, ${INPUT}"
ffmpeg -v quiet -y -vn -acodec pcm_s16le -ar 44100 -ac 2 $AUDIO -i $INPUT

# extract 2stems model
if [ ! -e "$(pwd)/pretrained_models/2stems" ]; then
  mkdir -p ./pretrained_models/2stems
  tar -zxf  /tmp/2stems.tar.gz -C ./pretrained_models/2stems
fi

if [ -f "$FOLDER/audio/vocals.wav" ]; then
  echo "Vocal exists, skip split ${AUDIO}"
else
  echo "Start spleeter."
  spleeter separate -p spleeter:2stems -o . $AUDIO
fi

rm -rf $OUTPUT
echo "Merging video+audio, ${OUTPUT}"
ffmpeg -v quiet -y -i $INPUT -itsoffset 0.3 -i "$FOLDER/audio/accompaniment.wav" -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac $OUTPUT

DURATION=$(($SECONDS - $START))
echo "Export to ${OUTPUT}."
echo "Processed in ${DURATION} seconds."
rm -rf ./pretrained_models

if [ -f "/whisper.sh" ]; then
  MODEL="${3:-medium}"
  LANG="${4:-Chinese}"
  /whisper.sh $VOCALS $MODEL $LANG
  if [ -f "${SUBTITLE}" ]; then
    echo "Merging video/audio/subtitle, ${OUTPUT}"
    ffmpeg -v quiet -y -i $INPUT -itsoffset 0.3 -i "$FOLDER/audio/accompaniment.wav" -vf "subtitles='${SUBTITLE}'" -c:v copy -map 0:v:0 -map 1:a:0 -c:a aac $SUBTITLE_VIDEO
  fi
fi

