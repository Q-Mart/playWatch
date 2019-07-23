import sounddevice as sd
import struct
import numpy as np
import matplotlib.pyplot as plt

from scipy.fftpack import fft

CHUNK = 1024 * 2
FORMAT = 'int16'
CHANNELS = 1
RATE = 44100

stream = sd.RawStream(
    samplerate=RATE,
    dtype=FORMAT,
    channels=CHANNELS,
    blocksize=CHUNK,
)

fig, (ax1, ax2) = plt.subplots(2)
fig.show()

x = np.arange(0, CHUNK)
x_fft = np.linspace(0, RATE, CHUNK)

line, = ax1.plot(x, np.random.rand(CHUNK))
line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-')

MAX_UINT16 = (2**15)-1
MIN_UINT16 = -MAX_UINT16

ax1.set_ylim(MIN_UINT16, MAX_UINT16)


with stream:
    while True:
        data = stream.read(CHUNK)[0][:]
        data_int = struct.unpack(str(CHUNK)+'h', data)
        # print(data_int)

        line.set_ydata(data_int)

        y_fft = fft(data_int)
        y_fft /= np.max(np.abs(y_fft))
        line_fft.set_ydata(np.abs(y_fft))

        fig.canvas.draw()
        fig.canvas.flush_events()
