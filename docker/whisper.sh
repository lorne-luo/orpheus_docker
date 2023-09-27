#!/bin/bash

MODEL="${2:-large}"
LANG="${3:-Chinese}"

echo "Whisper ${1} with ${MODEL} model"
START=$SECONDS

init=""
if [[ $LANG == "Chinese" || $LANG == "zh" ]]; then
    init="这是一首简体中文普通话的歌。"
fi
if [[ $LANG == "English" || $LANG == "en" ]]; then
    init="This is a english song."
fi

whisper $1 --model $MODEL --language $LANG --initial_prompt "'${init}'"
opencc -c t2s -i vocals.srt -o vocals.srt
opencc -c t2s -i vocals.json -o vocals.json
opencc -c t2s -i vocals.tsv -o vocals.tsv
opencc -c t2s -i vocals.txt -o vocals.txt
opencc -c t2s -i vocals.vtt -o vocals.vtt

python3 /srt2ass.py $(pwd)/vocals.srt $(pwd)/vocals.ass
python3 /subtitle_effects.py $(pwd)/vocals.ass $(pwd)/vocals_fx.ass

DURATION=$(($SECONDS - $START))
echo "Whisper in ${DURATION} seconds."
