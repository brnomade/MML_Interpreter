import winsound
import time
import ply.lex as lex


class SoundUtils:

    def __init__(self):
        self._notes = dict()
        self._notes[1] = {"C": 16.35, "D": 18.35, "E": 20.60, "F": 21.83, "G": 24.50, "A": 27.50, "B": 30.87}
        self._k = {"#": 1.0594631, "-": 1.0 / 1.0594631, "": 1}
        self._octave = 1
        self._rhythm = 1
        for o in range(2, 11):
            self._notes[o] = dict()
            for n in "CDEFGAB":
                self._notes[o][n] = self._calculate_frequency(o, n)

    def _calculate_frequency(self, octave, note, k=""):
        return round(self._notes[1][note] * (2 ** (octave - 1)) * self._k[k], 2)

    @property
    def rhythm(self):
        return self._rhythm

    @rhythm.setter
    def rhythm(self, a_value):
        self._rhythm = 2.0 * (1.0 / a_value)

    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, a_value):
        if a_value < 1 or a_value > 10:
            raise ValueError
        self._octave = a_value

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, a_value):
        self._k = a_value

    def pause_in_rhythm(self, a_value):
        return round(self._rhythm * (2000.0 * (1.0 / a_value)))

    def duration_in_rhythm(self, a_value):
        return round(self._rhythm * (4000.0 * (1.0 / a_value)))

    def compute_frequency_for_note(self, note, accident=""):
        return round(self._notes[self.octave][note] * self._k[accident])

    def reset(self):
        self.__init__()


class MSXMMLLexer:
    tokens = [
        'OPERATOR_T',
        'OPERATOR_V',
        'OPERATOR_R',
        'OCTAVE',
        'LENGTH',
        'OPERATOR_S',
        'OPERATOR_M',
        'OPERATOR_Y',
        'OPERATOR_HILOW',
        'NOTE_NUMERIC',
        'NOTE_ALFA'
    ]

    t_ignore = '; \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def _no_argument_tuple(self, token):
         return {"operator": token.value[0], "argument": None, "value": token.value}

    def _single_numeric_argument_tuple(self, token):
        if len(token.value) == 1:
            argument = None
        else:
            argument = int(token.value[1:])
        return {"operator": token.value[0], "argument": argument, "value": token.value}

    def _double_argument_tuple(self, token):
        many_dots = token.value.count(".")
        if many_dots == 0:
            argument = token.value[1:]
        else:
            argument = token.value[1:token.value.find(".")]
        return {"operator": token.value[0], "argument": int(argument), "dots": many_dots, "value": token.value}

    def _variable_double_argument_tuple(self, token):
        many_dots = token.value.count(".")
        temp_token = token.value.replace(".", "")
        if len(temp_token[1:]) == 0:
            argument = None
        else:
            argument = int(temp_token[1:])
        return {"operator": token.value[0], "argument": argument, "dots": many_dots, "value": token.value}

    def _variable_triple_argument_tuple(self, token):
        many_dots = token.value.count(".")
        temp_token = token.value.replace(".", "")
        accent = ""
        for c_to_find in "-+#":
            if temp_token.find(c_to_find) == 1:
                accent = c_to_find
                temp_token = temp_token.replace(c_to_find, "")
        if len(temp_token[1:]) == 0:
            argument = None
        else:
            argument = int(temp_token[1:])
        return {"operator": token.value[0], "accent": accent, "argument": argument,
                "dots": many_dots, "value": token.value
                }

    def t_NOTE_NUMERIC(self, t):
        r'[Nn]\d+\.*'
        t.value = self._double_argument_tuple(t)
        return t

    def t_NOTE_ALFA(self, t):
        r'[ABCDEFGabcdefg][-+#]*\d*\.*'
        t.value = self._variable_triple_argument_tuple(t)
        return t

    def t_OPERATOR_HILOW(self, t):
        r'[\>\<]'
        t.value = self._no_argument_tuple(t)
        return t

    def t_OPERATOR_R(self, t):
        r'[Rr]\d*\.*'
        t.value = self._variable_double_argument_tuple(t)
        return t

    def t_OPERATOR_T(self, t):
        r'[Tt]\d*'
        #if len(t.value) == 1:
        #    t.value = self._no_argument_tuple(t)
        #else:
        #    t.value = self._single_numeric_argument_tuple(t)
        t.value = self._single_numeric_argument_tuple(t)
        return t

    def t_OPERATOR_V(self, t):
        r'[Vv]\d*'
        if len(t.value) == 1:
            t.value = self._no_argument_tuple(t)
        else:
            t.value = self._single_numeric_argument_tuple(t)
        return t

    def t_LENGTH(self, t):
        r'[Ll]\d*'
        if len(t.value) == 1:
            t.value = self._no_argument_tuple(t)
        else:
            t.value = self._single_numeric_argument_tuple(t)
        return t

    def t_OPERATOR_S(self, t):
        r'[Ss]\d*'
        if len(t.value) == 1:
            t.value = self._no_argument_tuple(t)
        else:
            t.value = self._single_numeric_argument_tuple(t)
        return t

    def t_OPERATOR_M(self, t):
        r'[Mm]\d*'
        if len(t.value) == 1:
            t.value = self._no_argument_tuple(t)
        else:
            t.value = self._single_numeric_argument_tuple(t)
        return t

    def t_OCTAVE(self, t):
        r'[Oo]\d+'
        if len(t.value) == 1:
            raise NotImplementedError
        else:
            t.value = self._single_numeric_argument_tuple(t)
        return t

    def t_OPERATOR_Y(self, t):
        r'[Yy]\d+'
        if len(t.value) == 1:
            raise NotImplementedError
        else:
            t.value = self._single_numeric_argument_tuple(t)
        return t

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def set_input(self, input_string):
        self.lexer.input(input_string)

    def get_token(self):
        return self.lexer.token()



class MSXMMLParser:

    def __init__(self):
        self._lexer = MSXMMLLexer()

    def compile(self, input_string):
        self._lexer.set_input(input_string)
        su = SoundUtils()
        sp = SynchronousPlayer()
        duration = 200
        while True:
            mml_token = self._lexer.get_token()
            if not mml_token:
                break  # No more input
            if mml_token.type == "NOTE_ALFA":
                f = su.compute_frequency_for_note(mml_token.value["operator"], mml_token.value["accent"])
                extra_duration = mml_token.value["dots"] * round(duration / 2)
                sp.play(f, duration + extra_duration)
            elif mml_token.type == "OCTAVE":
                su.octave = mml_token.value["argument"]
            elif mml_token.type == "LENGTH" and mml_token.value["argument"] is not None:
                duration = su.duration_in_rhythm(mml_token.value["argument"])


            # if mml_token.type == "OPERATOR_T":
            #     print("operator T", mml_token.value)
            # elif mml_token.type == "OPERATOR_V":
            #     print("operator V", mml_token.value)
            # elif mml_token.type == "OPERATOR_R":
            #     print("operator R", mml_token.value)
            # elif mml_token.type == "OPERATOR_O":
            #     print("operator O", mml_token.value)
            # elif mml_token.type == "OPERATOR_N":
            #     print("operator N", mml_token.value)
            # elif mml_token.type == "OPERATOR_L":
            #     print("operator L", mml_token.value)
            # elif mml_token.type == "OPERATOR_S":
            #     print("operator S", mml_token.value)
            # elif mml_token.type == "OPERATOR_M":
            #     print("operator M", mml_token.value)
            # elif mml_token.type == "OPERATOR_Y":
            #     print("operator Y", mml_token.value)
            # elif mml_token.type == "OPERATOR_HILOW":
            #     print("operator HL", mml_token.value)
            # elif mml_token.type == "NOTE":
            #     print("Note", mml_token.value)
            # else:
            #     print("error", mml_token)


class SynchronousPlayer:

    def play(self, frequency, delay=200):
        if 37 < frequency < 32767:
            winsound.Beep(frequency, delay)


def main():
    print("start")
    sp = SynchronousPlayer()
    su = SoundUtils()
    for octave in range(1, 11):
        su.octave = octave
        for note in "CDEFGAB":
            tic1 = time.perf_counter()
            f1 = su.compute_frequency_for_note(note, "#")
            toc1 = time.perf_counter()
            print(octave - 1, note, f1, f"{toc1 - tic1:0.8f}")
            # sp.play(f)
    # msx_lex = MSXMMLLexer()
    msx_par = MSXMMLParser()
    #msx_par.compile(vampire_killer())
    msx_par.compile(bitmus())
    print("end")


def vampire_killer():
    voz1 = "t90;L16;V11;S0;M300;O5;D;D;R16;C;R16;O4;B;V13;B4;B;S0;D;V13;D;S0;E;F;G;A;V13;A8;S0;D;V13;D8;S0;A;V13;A;" \
           "S0;" \
           "G;O5;C;V13;C4.;S0;O5;D;D;R16;C;R16;O4;B;V13;B4;B;S0;D;V13;D;S0;E;F;G;A;V13;A8;S0;D;V13;D8;S0;A;V13;A;G;" \
           "O4;" \
           "C;V13;C4.;O5;R8;D;R8;A;V13;A8;S0;G#;A;G#;F;R;R8;F;D;V12;F;D;V11;F;D;V10;F;F;V9;D;F;R16;V8;F;D;F;V13;O5;" \
           "R8;" \
           "D;R8;A;V13;A8;S0;G#;A;G#;F;R;R8;F;D;V12;F;D;V11;D;F;V10;F;D;V9;F;R16;F;V8;D;F;C#;V13;C#8;S0;E;V13;E8;S0;" \
           "B-;" \
           "V13;B-;S0;A;V13;A8;S0;F;V13;F8;S0;D;V13;D;C#;V13;C#8;S0;E;V13;E8;S0;B-;V13;B-;S0;A;V13;A8;S0;D;R;C#;V13;" \
           "C#8;S0;E;V13;E8;S0;B-;V13;B-;S0;A;V13;A8;S0;F;V13;F8;S0;D;V13;D;S0;E;V13;E8;S0;G;V13;G8;S0;B-;V13;B-;S0;" \
           "A;V13;A8;S0;B;V13;B8;O6;S0;C#;V13;C#;S0;D;D;O5;D;V13;D;D8;R8;R2;O3;S0;B-;R16;B-;R16;O4;D;F;V13;F8;S0;C;" \
           "R16;C;R16;E;G;V13;G8;S0;S0;O6;D;D;O5;D;V13;D;D8;R8;R2;O3;S0;B-;R16;B-R16;O4;D;F;V13;F8;S0;C;R8.;O3;A;O4;" \
           "C;V13;C8"
    return voz1


def bitmus():
    voz1 = "T90L8V11O4F#4GF#EDC#EDEF#GA4BBDF#GEF#DEC#D" \
           "L16C#O3BAGF#EL8DABO4C#F#E16F#16GF#E"\
           "L16AGF#EDC#D8C#DEDC#O3BO4C#8O3BO4C#"\
           "D8C#8O3B8O4BAGF#EDC#O3BA#G#A#BO4C#O3"\
           "A#A#96B8O4F#8F#96G#8A#8A#96B2"

    voz2 = "T90L8V10O4D4DDC#DEC#DDO3AAF#4BO4C#DDEC#DAAGF#"\
           "L16F#F#DDDDR8L8C#DEDL16DDL8DDEL16EEEEEE"\
           "E8EEO3BBBBO4C#8C#C#D8C#8O3B8BBO4EEDDC#C#O3"\
           "BBO4C#C#C#C#C#96O3B8B8B96B8B8B96R2"

    voz3 = "t90l4v10o3al8aaaaaadddr4ggf#f#eeo4ddc#c#o3al16aar16r16r16r16l8a"\
           "r8r8r8f#l16f#f#l8ddal16aaaaaal8f#l16f#f#o2ggggo3l8"\
           "f#l16f#f#l8f#f#g#l16eer16r16r16r16f#f#f#f#f#f#f#f#r96"\
           "l8f#f#l96f#l8f#f#l96f#l2f#"
    return voz1

main()



