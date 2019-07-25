from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys

import sounddevice as sd
import struct
from scipy.fftpack import fft

class Plot2D(object):
    def __init__(self):
        self.traces = dict()

        self.phase = 0
        self.t = np.arange(0, 3.0, 0.01)

        pg.setConfigOptions(antialias=True)
        self.app = QtGui.QApplication(sys.argv)
        self.win = pg.GraphicsWindow(title='Audio Analyser')
        self.win.resize(1000, 600)
        self.win.setWindowTitle('Audio Analyser')

        self.waveform = self.win.addPlot(title='WAVEFORM', row=1, col=1)
        self.spectrum = self.win.addPlot(title='SPECTRUM', row=2, col=1)

        self.MAX_UINT16 = (2**15)-1
        self.MIN_UINT16 = -self.MAX_UINT16

        self.CHUNK = 1024 * 2
        self.FORMAT = 'int16'
        self.CHANNELS = 1
        self.RATE = 44100

        self.x = np.arange(0, self.CHUNK)
        self.f = np.linspace(0, self.RATE, self.CHUNK)

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec()

    def set_plotdata(self, name, dataset_x, dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x, dataset_y)
        elif name == 'waveform':
            self.traces[name] = self.waveform.plot(pen='c', width=3)
            self.waveform.setYRange(self.MIN_UINT16, self.MAX_UINT16, padding=0)
            self.waveform.setXRange(0, self.CHUNK, padding=0.005)
        elif name == 'spectrum':
            self.traces[name] = self.spectrum.plot(pen='m', width=3)
            self.spectrum.setLogMode(x=True, y=True)
            self.spectrum.setYRange(-4, 0, padding=0)
            self.spectrum.setXRange(
                np.log10(20), np.log10(self.RATE / 2), padding=0.005
            )

    def update(self):
        self.stream = sd.Stream(
            samplerate=self.RATE,
            dtype=self.FORMAT,
            channels=self.CHANNELS,
            blocksize=self.CHUNK,
            )

        with self.stream:
            wf_data = self.stream.read(self.CHUNK)[0][:]

        wf_data = struct.unpack(str(self.CHUNK)+'h', wf_data)
        self.set_plotdata(name='waveform', dataset_x=self.x, dataset_y=wf_data)

        sp_data = fft(wf_data)
        sp_data = np.abs(sp_data)
        sp_data /= np.max(np.abs(sp_data))
        self.set_plotdata(name='spectrum', dataset_x=self.f, dataset_y=sp_data)

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()


if __name__ == '__main__':
    p = Plot2D()
    p.animation()
