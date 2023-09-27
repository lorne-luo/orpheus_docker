import os
import sys
from pyonfx import Ass, Utils, Shape, ColorUtility, FrameUtility, Convert

import random
import math


class SubtitleFX:
    def __init__(self, input_file, output_file=None):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f'SubtitleFX: {input_file} not exist.')

        self.work_dir = os.path.dirname(input_file)
        if not output_file:
            self.output_file = os.path.join(self.work_dir, 'output.ass')
        elif not os.path.dirname(output_file) != '':
            self.output_file = os.path.join(self.work_dir, output_file)
        else:
            self.output_file = output_file

        self.io = Ass(input_file, path_output=self.output_file)
        meta, styles, self.lines = self.io.get_data()
        self.star = Shape.star(5, 4, 10)
        self.CU = ColorUtility(self.lines)

    def romaji(self, line, l):
        # Setting up a delay, we will use it as duration time of the feadin and feadout effects
        delay = 300
        # Setting up offset variables, we will use them for the \move in leadin and leadout effects
        off_x = 35
        off_y = 15

        # Leadin Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0

            l.start_time = (
                    line.start_time + 25 * syl.i - delay - 80
            )  # Remove 80 to start_time to let leadin finish a little bit earlier than the main effect of the first syllable
            l.end_time = line.start_time + syl.start_time
            l.dur = l.end_time - l.start_time

            l.text = (
                    "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,0,%d)\\blur2\\t(0,%d,\\blur0)\\fad(%d,0)}%s"
                    % (
                        syl.center + math.cos(syl.i / 2) * off_x,
                        syl.middle + math.sin(syl.i / 4) * off_y,
                        syl.center,
                        syl.middle,
                        delay,
                        delay,
                        delay,
                        syl.text,
                    )
            )

            self.io.write_line(l)

        # Main Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 1

            l.start_time = line.start_time + syl.start_time
            l.end_time = line.start_time + syl.end_time + 100
            l.dur = l.end_time - l.start_time

            c1 = "&H81F4FF&"
            c3 = "&H199AAA&"

            # Change color if inline_fx is m1
            if syl.inline_fx == "m1":
                c1 = "&H8282FF&"
                c3 = "&H191AAA&"

            on_inline_effect_2 = ""
            # Apply rotation if inline_fx is m2
            if syl.inline_fx == "m2":
                on_inline_effect_2 = "\\t(0,%d,\\frz%.3f)\\t(%d,%d,\\frz0)" % (
                    l.dur / 4,
                    random.uniform(-40, 40),
                    l.dur / 4,
                    l.dur,
                )

            l.text = (
                    "{\\an5\\pos(%.3f,%.3f)%s\\t(0,80,\\fscx105\\fscy105\\1c%s\\3c%s)\\t(80,%d,\\fscx100\\fscy100\\1c%s\\3c%s)}%s"
                    % (
                        syl.center,
                        syl.middle,
                        on_inline_effect_2,
                        c1,
                        c3,
                        l.dur - 80,
                        line.styleref.color1,
                        line.styleref.color3,
                        syl.text,
                    )
            )

            self.io.write_line(l)

            # Animating star shape that jumps over the syllables
            # Jump-in to the first syl
            jump_height = 18
            if syl.i == 0:
                FU = FrameUtility(line.start_time - line.leadin / 2, line.start_time)
                for s, e, i, n in FU:
                    l.start_time = s
                    l.end_time = e
                    frame_pct = i / n

                    x = syl.center - syl.width * (1 - frame_pct)
                    y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                    alpha = 255
                    alpha += FU.add(0, syl.duration, -255)
                    alpha = Convert.alpha_dec_to_ass(int(alpha))

                    l.text = (
                            "{\\alpha%s\\pos(%.3f,%.3f)\\bord1\\blur1\\1c%s\\3c%s\\p1}%s"
                            % (alpha, x, y, c1, c3, self.star)
                    )
                    self.io.write_line(l)

            # Jump to the next syl or to the end of line
            jump_width = (
                line.syls[syl.i + 1].center - syl.center
                if syl.i != len(line.syls) - 1
                else syl.width
            )
            FU = FrameUtility(
                line.start_time + syl.start_time, line.start_time + syl.end_time
            )
            for s, e, i, n in FU:
                l.start_time = s
                l.end_time = e
                frame_pct = i / n

                x = syl.center + frame_pct * jump_width
                y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                alpha = 0
                # Last jump should fade-out
                if syl.i == len(line.syls) - 1:
                    alpha += FU.add(0, syl.duration, 255)
                alpha = Convert.alpha_dec_to_ass(int(alpha))

                l.text = "{\\alpha%s\\pos(%.3f,%.3f)\\bord1\\blur1\\1c%s\\3c%s\\p1}%s" % (
                    alpha,
                    x,
                    y,
                    c1,
                    c3,
                    self.star,
                )
                self.io.write_line(l)

        # Leadout Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0

            l.start_time = line.start_time + syl.end_time + 100
            l.end_time = line.end_time - 25 * (len(line.syls) - syl.i) + delay + 100
            l.dur = l.end_time - l.start_time

            l.text = (
                    "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,%d,%d)\\t(%d,%d,\\blur2)\\fad(0,%d)}%s"
                    % (
                        syl.center,
                        syl.middle,
                        syl.center + math.cos(syl.i / 2) * off_x,
                        syl.middle + math.sin(syl.i / 4) * off_y,
                        l.dur - delay,
                        l.dur,
                        l.dur - delay,
                        l.dur,
                        delay,
                        syl.text,
                    )
            )

            self.io.write_line(l)

    def kanji(self, line, l):
        # Setting up a delay, we will use it as duration time of the leadin and leadout effects
        delay = 400
        # Setting up offset variables, we will use them for the \move in leadin and leadout effects
        off_x = 35
        off_y = 15

        # Leadin Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0
            pos_x = syl.center
            pos_y = syl.middle * 0.8

            l.start_time = (
                    line.start_time + 25 * syl.i - delay - 80
            )
            # Remove 80 to start_time to let leadin finish a little bit earlier than the main effect of the first syllable
            l.end_time = line.start_time + syl.start_time
            l.dur = l.end_time - l.start_time

            l.text = (
                    "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,0,%d)\\blur2\\t(0,%d,\\blur0)\\fad(%d,0)}%s"
                    % (
                        pos_x + math.cos(syl.i / 2) * off_x,
                        pos_y + math.sin(syl.i / 4) * off_y,
                        pos_x,
                        pos_y,
                        delay,
                        delay,
                        delay,
                        syl.text,
                    )
            )

            self.io.write_line(l)

        # Main Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 1
            pos_x = syl.center
            pos_y = syl.middle * 0.8

            l.start_time = line.start_time + syl.start_time
            l.end_time = line.start_time + syl.end_time + 100
            l.dur = l.end_time - l.start_time

            c1 = "&H81F4FF&"
            c3 = "&H199AAA&"
            # Change color if effect field is m1
            if line.effect == "m1":
                c1 = "&H8282FF&"
                c3 = "&H191AAA&"

            on_inline_effect_2 = ""
            # Apply rotation if effect field is m2
            if line.effect == "m2":
                on_inline_effect_2 = "\\t(0,%d,\\frz%.3f)\\t(%d,%d,\\frz0)" % (
                    l.dur / 4,
                    random.uniform(-40, 40),
                    l.dur / 4,
                    l.dur,
                )

            l.text = (
                    "{\\an5\\pos(%.3f,%.3f)%s\\t(0,80,\\fscx105\\fscy105\\1c%s\\3c%s)\\t(80,%d,\\fscx100\\fscy100\\1c%s\\3c%s)}%s"
                    % (
                        pos_x,
                        pos_y,
                        on_inline_effect_2,
                        c1,
                        c3,
                        l.dur - 80,
                        line.styleref.color1,
                        line.styleref.color3,
                        syl.text,
                    )
            )

            self.io.write_line(l)

        # Leadout Effect
        for syl in Utils.all_non_empty(line.syls):
            l.layer = 0
            pos_x = syl.center
            pos_y = syl.middle * 0.8

            l.start_time = line.start_time + syl.end_time + 100
            l.end_time = line.end_time - 25 * (len(line.syls) - syl.i) + delay + 100
            l.dur = l.end_time - l.start_time

            l.text = (
                    "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,%d,%d)\\t(%d,%d,\\blur2)\\fad(0,%d)}%s"
                    % (
                        pos_x,
                        pos_y,
                        pos_x + math.cos(syl.i / 2) * off_x,
                        pos_y + math.sin(syl.i / 4) * off_y,
                        l.dur - delay,
                        l.dur,
                        l.dur - delay,
                        l.dur,
                        delay,
                        syl.text,
                    )
            )

            self.io.write_line(l)

    def sub(self, line, l):
        # Translation Effect
        l.layer = 0

        l.start_time = line.start_time - line.leadin / 2
        l.end_time = line.end_time + line.leadout / 2
        l.dur = l.end_time - l.start_time

        # Getting interpolated color changes (notice that we do that only after having set up all the times, that's important)
        colors = self.CU.get_color_change(l)

        # Base text
        l.text = "{\\an5\\pos(%.3f,%.3f)\\fad(%d,%d)}%s" % (
            line.center,
            line.middle,
            line.leadin / 2,
            line.leadout / 2,
            line.text,
        )
        self.io.write_line(l)

        # Random clipped text colorated
        l.layer = 1
        for i in range(1, int(line.width / 80)):
            x_clip = line.left + random.uniform(0, line.width)
            y_clip = line.top - 5

            clip = (
                x_clip,
                y_clip,
                x_clip + random.uniform(10, 30),
                y_clip + line.height + 10,
            )

            l.text = "{\\an5\\pos(%.3f,%.3f)\\fad(%d,%d)\\clip(%d,%d,%d,%d)%s}%s" % (
                line.center,
                line.middle,
                line.leadin / 2,
                line.leadout / 2,
                clip[0],
                clip[1],
                clip[2],
                clip[3],
                colors,
                line.text,
            )
            self.io.write_line(l)

    def run(self):
        """"""
        for line in self.lines:
            # Generating lines
            if line.styleref.name == 'Romaji':
                self.romaji(line, line.copy())
            elif line.styleref.name == 'Kanji':
                self.kanji(line, line.copy())
            else:
                self.sub(line, line.copy())

        self.io.save()
        # self.io.open_aegisub()

        print(f'#6 generate subtitle file: {self.output_file}')


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv)>2 else None
    SubtitleFX(input_path, output_path).run()