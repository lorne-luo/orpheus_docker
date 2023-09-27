import sys
import os
import re
import codecs
from datetime import datetime, timedelta


def str2delta(duration_string):
    # Parse the duration string using strptime
    # The format string matches the input format
    duration = datetime.strptime(duration_string, "%H:%M:%S,%f")

    # Convert the datetime object to a timedelta
    time_delta = timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second,
                           microseconds=duration.microsecond)

    return time_delta


def fileopen(input_file):
    encodings = ["utf-32", "utf-16", "utf-8", "cp1252", "gb2312", "gbk", "big5"]
    tmp = ''
    for enc in encodings:
        try:
            with codecs.open(input_file, mode="r", encoding=enc) as fd:
                tmp = fd.read()
                break
        except:
            # print enc + ' failed'
            continue
    return [tmp, enc]


def srt2ass(input_file):
    if '.ass' in input_file:
        return input_file

    if not os.path.isfile(input_file):
        print(input_file + ' not exist')
        return

    src = fileopen(input_file)
    tmp = src[0]
    encoding = src[1]
    src = ''
    utf8bom = ''

    if u'\ufeff' in tmp:
        tmp = tmp.replace(u'\ufeff', '')
        utf8bom = u'\ufeff'

    tmp = tmp.replace("\r", "")
    lines = [x.strip() for x in tmp.split("\n") if x.strip()]
    subLines = ''
    tmpLines = ''
    lineCount = 0
    output_file = '.'.join(input_file.split('.')[:-1])
    output_file += '.ass'

    for ln in range(len(lines)):
        line = lines[ln]
        if line.isdigit() and re.match('-?\d\d:\d\d:\d\d', lines[(ln + 1)]):
            if tmpLines:
                subLines += tmpLines + "\n"
            tmpLines = ''
            lineCount = 0
            continue
        else:
            if re.match('-?\d\d:\d\d:\d\d', line):
                line = line.replace('-0', '0')
                start, end = line.split(' --> ')
                start = datetime.strptime(start, "%H:%M:%S,%f")
                end = datetime.strptime(end, "%H:%M:%S,%f")
                duration = end - start
                start -= timedelta(microseconds=0.2 * 1000000)
                end -= timedelta(seconds=duration.total_seconds() * .15)
                line = start.strftime("%H:%M:%S,%f") + ',' + end.strftime("%H:%M:%S,%f")
                tmpLines += 'Dialogue: 0,' + line + ',Kanji,,0,0,0,,{\k100}'
            else:
                if lineCount < 2:
                    tmpLines += line
                else:
                    tmpLines += "\n" + line
            lineCount += 1
        ln += 1

    subLines += tmpLines + "\n"

    subLines = re.sub(r'\d(\d:\d{2}:\d{2}),(\d{2})\d', '\\1.\\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)

    # replace style
    subLines = re.sub(r'<([ubi])>', "{\\\\\g<1>1}", subLines)
    subLines = re.sub(r'</([ubi])>', "{\\\\\g<1>0}", subLines)
    subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', "{\\\\c&H\\3\\2\\1&}", subLines)
    subLines = re.sub(r'</font>', "", subLines)

    head_str = '''[Script Info]
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,8,25,25,25,1
Style: Romaji,Migu 1P,48,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,8,25,25,25,1
Style: Translation,Migu 1P,46,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,2,25,25,25,1
Style: Kanji,Migu 1P,78,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.8,0,2,25,25,25,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'''

    output_str = utf8bom + head_str + '\n' + subLines
    output_str = output_str.encode(encoding)

    print(f'Output to {output_file}')
    with open(output_file, 'wb') as output:
        output.write(output_str)

    output_file = output_file.replace('\\', '\\\\')
    output_file = output_file.replace('/', '//')
    return output_file


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for name in sys.argv[1:]:
            srt2ass(name)
