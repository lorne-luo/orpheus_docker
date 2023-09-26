#!/bin/bash
# Youtube video url or id to karaoke video

# Enable strict mode (halt on error and unset variable)
set -euo pipefail

# Function to check if a URL is valid
is_valid_url() {
  local url="$1"
  if [[ "$url" =~ ^https?:// ]]; then
    echo 0
  else
    echo 1
  fi
}

START=$SECONDS
URL=$1

if [ $(is_valid_url "$1") -gt 0 ]; then
  ID=$1
  URL="https://www.youtube.com/watch?v=${1}"
else
  ID=$(yt-dlp --print filename -o "%(id)s" ${1})
fi

#if [ -z "${2:-}" ]; then
#  OUTPUT="/data/${ID}/${ID}_ok.mp4"
#else
#  if [[ "$2" != *.* ]]; then
#    OUTPUT="/data/${ID}/${2}.mp4"
#  else
#    OUTPUT="/data/${ID}/${2}"
#  fi
#fi

mkdir -p "/data/${ID}"
OUTPUT="/data/${ID}/${ID}_ok.mp4"
DOWNLOAD="/data/${ID}/${ID}.mp4"

if [ -f "$DOWNLOAD" ]; then
  echo "$DOWNLOAD exists."
else
  #echo "URL=$URL"
  #echo "ID=$ID"
  echo "DOWNLOAD=$DOWNLOAD"
  echo "OUTPUT=$OUTPUT"
  yt-dlp -N 1 --no-playlist -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "/data/%(id)s/%(id)s.mp4" $URL

  DURATION=$(($SECONDS - $START))
  echo "Download from Youtube in ${DURATION} seconds."
fi

MODEL="${2:-medium}"
LANG="${3:-Chinese}"
/v2ok.sh $DOWNLOAD $OUTPUT $MODEL $LANG
DURATION=$(($SECONDS - $START))
echo "Finished in ${DURATION} seconds."
