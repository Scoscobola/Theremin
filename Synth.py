import multiprocessing
from pyo import *


def generateScale(key, quality):
    if quality.lower() == "major":
        return [key, key + 2, key + 4, key + 5, key + 7, key + 9, key + 11, key + 12]
    elif quality.lower() == "minor":
        return [key, key + 2, key + 3, key + 5, key + 7, key + 8, key + 11, key + 12]


def nameToMidi(name, octave):
    c = 24
    if name == 'C':
        return c + (12 * octave)
    elif name == 'C#/Db':
        return (c + 1) + (12 * octave)
    elif name == 'D':
        return (c + 2) + (12 * octave)
    elif name == 'D#/Eb':
        return (c + 3) + (12 * octave)
    elif name == 'E':
        return (c + 4) + (12 * octave)
    elif name == 'F':
        return (c + 5) + (12 * octave)
    elif name == 'F#/Gb':
        return (c + 6) + (12 * octave)
    elif name == 'G':
        return (c + 7) + (12 * octave)
    elif name == 'G#/Ab':
        return (c + 8) + (12 * octave)
    elif name == 'A':
        return (c + 9) + (12 * octave)
    elif name == 'A#/Bb':
        return (c + 10) + (12 * octave)
    elif name == 'B':
        return (c + 11) + (12 * octave)


class SynthProc(multiprocessing.Process):
    def __init__(self, f_queue, c_queue, key, size=None, quality="major"):
        super(SynthProc, self).__init__()
        self.f_queue = f_queue
        self.c_queue = c_queue
        self.key = key
        self.scale = generateScale(self.key, quality)

        if size is None:
            self.size = (720, 1280)
        else:
            self.size = size

    def setScale(self, key, quality):
        self.scale = generateScale(key, quality)

    def convertRootToMidi(self, pos):
        value = int(((len(self.scale) / self.size[1]) * pos))
        return self.scale[value]

    def convertChordToneToFreq(self, root, tone, quality):
        if tone == 1:
            return midiToHz(root)
        elif tone == 3:
            if quality == 1:
                return midiToHz(root + 4)
            else:
                return midiToHz(root + 3)
        elif tone == 5:
            if quality == 1:
                return midiToHz(root + 7)
            else:
                return midiToHz(root + 6)
        elif tone == 7:
            if quality == 1:
                return midiToHz(root + 11)
            else:
                return midiToHz(root + 10)

    def convertToAmp(self, pos):
        if pos == 0:
            return 0

        return abs(1.0 / 720 * (pos - self.size[0]))

    def run(self):
        self.server = Server()
        self.server.setOutputDevice(1)
        self.server.boot()
        self.freqs = []
        self.oscs = []
        for i in range(4):
            self.freqs.append(SigTo(value=0, time=0.005))
            self.oscs.append([FastSine(freq=self.freqs[i]).out(), FastSine(freq=self.freqs[i]).out(1)])

        self.server.amp = 0.1
        self.server.start()
        while True:
            if not self.c_queue.empty():
                controlData = self.c_queue.get()

                if len(controlData) == 3:
                    self.setScale(nameToMidi(controlData[0], controlData[1]), controlData[2])
                else:
                    self.c_queue.put(controlData)

            if not self.f_queue.empty():
                posData = self.f_queue.get()
                midiRoot = self.convertRootToMidi(posData[0])
                rootAmp = self.convertToAmp(posData[1])
                thirdAmp = self.convertToAmp(posData[3])
                fifthAmp = self.convertToAmp(posData[5])
                seventhAmp = self.convertToAmp(posData[7])
                self.freqs[0].value = self.convertChordToneToFreq(midiRoot, 1, 1)
                self.freqs[1].value = self.convertChordToneToFreq(midiRoot, 3, posData[2])
                self.freqs[2].value = self.convertChordToneToFreq(midiRoot, 5, posData[4])
                self.freqs[3].value = self.convertChordToneToFreq(midiRoot, 7, posData[6])

                self.oscs[0][0].mul = rootAmp
                self.oscs[0][1].mul = rootAmp
                self.oscs[1][0].mul = thirdAmp
                self.oscs[1][1].mul = thirdAmp
                self.oscs[2][0].mul = fifthAmp
                self.oscs[2][1].mul = fifthAmp
                self.oscs[3][0].mul = seventhAmp
                self.oscs[3][1].mul = seventhAmp
