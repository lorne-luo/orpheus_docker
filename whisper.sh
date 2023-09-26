#!/bin/bash

MODEL="${2:-large}"
LANG="${3:-Chinese}"

whisper $1 --model $MODEL --language $LANG
opencc -c t2s -i vocals.srt -o vocals.srt
opencc -c t2s -i vocals.json -o vocals.json
opencc -c t2s -i vocals.tsv -o vocals.tsv
opencc -c t2s -i vocals.txt -o vocals.txt
opencc -c t2s -i vocals.vtt -o vocals.vtt