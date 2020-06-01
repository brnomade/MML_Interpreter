import winsound
import time


class SoundUtils:

    def __init__(self):
        self._notes = dict()
        self._notes[1] = {"C": 16.35, "D": 18.35, "E": 20.60, "F": 21.83, "G": 24.50, "A": 27.50, "B": 30.87}
        self._k = {"#": 1.0594631, "b": 1.0 / 1.0594631, "": 1}
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
        return round(self._rhythm * (2000.0 * (1.0 / a_value)))

    def compute_frequency_for_note(self, note, accident=""):
        return round(self._notes[self.octave][note] * self._k[accident])

    def reset(self):
        self.__init__()


class MMLSymbol:
    pass


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

    print("end")


def vampire_killer():
    voz1 = "t90;L16;V11;S0;M3000;O5;D;D;R16;C;R16;O4;B;V13;B4;B;S0;D;V13;D;S0;E;F;G;A;V13;A8;S0;D;V13;D8;S0;A;V13;A;" \
           "S0;" \
           "G;O5;C;V13;C4.;S0;O5;D;D;R16;C;R16;O4;B;V13;B4;B;S0;D;V13;D;S0;E;F;G;A;V13;A8;S0;D;V13;D8;S0;A;V13;A;G;" \
           "O4;" \
           "C;V13;C4.;O5;R8;D;R8;A;V13;A8;S0;G#;A;G#;F;R;R8;F;D;V12;F;D;V11;F;D;V10;F;F;V9;D;F;R16;V8;F;D;F;V13;O5;" \
           "R8;" \
           "D;R8;A;V13;A8;S0;G#;A;G#;F;R;R8;F;D;V12;F;D;V11;D;F;V10;F;D;V9;F;R16;F;V8;D;F;C#;V13;C#8;S0;E;V13;E8;S0;" \
           "Bb;" \
           "V13;Bb;S0;A;V13;A8;S0;F;V13;F8;S0;D;V13;D;C#;V13;C#8;S0;E;V13;E8;S0;Bb;V13;Bb;S0;A;V13;A8;S0;D;R;C#;V13;" \
           "C#8;S0;E;V13;E8;S0;Bb;V13;Bb;S0;A;V13;A8;S0;F;V13;F8;S0;D;V13;D;S0;E;V13;E8;S0;G;V13;G8;S0;Bb;V13;Bb;S0;" \
           "A;V13;A8;S0;B;V13;B8;O6;S0;C#;V13;C#;S0;D;D;O5;D;V13;D;D8;R8;R2;O3;S0;Bb;R16;Bb;R16;O4;D;F;V13;F8;S0;C;" \
           "R16;C;R16;E;G;V13;G8;S0;S0;O6;D;D;O5;D;V13;D;D8;R8;R2;O3;S0;Bb;R16;Bb;R16;O4;D;F;V13;F8;S0;C;R8.;O3;A;O4;" \
           "C;V13;C8"


main()



