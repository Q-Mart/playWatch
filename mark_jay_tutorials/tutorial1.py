import sounddevice as sd
import struct
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024 * 4
FORMAT = 'int16'
CHANNELS = 1
RATE = 44100

stream = sd.RawStream(
    samplerate=RATE,
    dtype=FORMAT,
    channels=CHANNELS,
    blocksize=CHUNK,
)

fig, ax = plt.subplots()
fig.show()

x = np.arange(0, CHUNK)
line, = ax.plot(x, np.random.rand(CHUNK))

MAX_UINT16 = (2**15)-1
MIN_UINT16 = -MAX_UINT16

ax.set_ylim(MIN_UINT16, MAX_UINT16)


with stream:
    while True:
        data = stream.read(CHUNK)[0][:]
        data_int = struct.unpack(str(CHUNK)+'h', data)
        # print(data_int)

        line.set_ydata(data_int)
        fig.canvas.draw()
        fig.canvas.flush_events()
