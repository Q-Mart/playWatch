import sounddevice as sd
import struct
import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import fft

class AudioPlotter(object):

    def __init__(self):
        self.MAX_UINT16 = (2**15)-1
        self.MIN_UINT16 = -self.MAX_UINT16

        self.CHUNK = 1024 * 2
        self.FORMAT = 'int16'
        self.CHANNELS = 1
        self.RATE = 44100

        self.stream = sd.RawStream(
            samplerate=self.RATE,
            dtype=self.FORMAT,
            channels=self.CHANNELS,
            blocksize=self.CHUNK,
            )

        self.init_plots()
        self.start_plots()

    def init_plots(self):
        self.fig, (ax1, ax2) = plt.subplots(2)
        self.fig.show()

        x = np.arange(0, self.CHUNK)
        x_fft = np.linspace(0, self.RATE, self.CHUNK)

        self.line, = ax1.plot(x, np.random.rand(self.CHUNK))
        self.line_fft, = ax2.semilogx(x_fft, np.random.rand(self.CHUNK), '-')


        ax1.set_ylim(self.MIN_UINT16, self.MAX_UINT16)


    def start_plots(self):
        with self.stream:
            while True:
                data = self.stream.read(self.CHUNK)[0][:]
                data_int = struct.unpack(str(self.CHUNK)+'h', data)
                # print(data_int)

                self.line.set_ydata(data_int)

                y_fft = fft(data_int)
                y_fft /= np.max(np.abs(y_fft))
                self.line_fft.set_ydata(np.abs(y_fft))

                self.fig.canvas.draw()
                self.fig.canvas.flush_events()

if __name__ == '__main__':
    AudioPlotter()
