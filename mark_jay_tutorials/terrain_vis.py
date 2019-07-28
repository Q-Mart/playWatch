# tutorial 5 (6th video)

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
from opensimplex import OpenSimplex
import sounddevice as sd
import struct

class Terrain(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window = gl.GLViewWidget()
        self.window.setGeometry(0, 100, 1920, 1080)
        self.window.show()
        self.window.setWindowTitle('Terrain')
        self.window.setCameraPosition(distance=30, elevation=8)

        # grid = gl.GLGridItem()
        # grid.scale(2, 2, 2)
        # self.window.addItem(grid)

        self.NSTEPS = 1.3
        self.ypoints = np.arange(-20, 20 + self.NSTEPS, self.NSTEPS)
        self.xpoints = np.arange(-20, 20 + self.NSTEPS, self.NSTEPS)
        self.nfaces = len(self.ypoints)
        self.offset = 0

        self.RATE = 44100
        self.CHUNK = len(self.xpoints) * len(self.ypoints)
        self.FORMAT = 'int16'
        self.CHANNELS = 1

        self.stream = None

        # Colours to match the ENSWBL asthetic
        self.startR = 0.2
        self.startG = 0.2
        self.startB = 0.2

        self.endR = 96.4 / 255
        self.endG = 0 / 255
        self.endB = 100 / 255

        self.rStep = (self.endR - self.startR) / 20
        self.gStep = (self.endG - self.startG) / 20
        self.bStep = (self.endB - self.startB) / 20

        self.open_simplex = OpenSimplex()

        verts, faces, colours = self.mesh()

        self.mesh1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces,
            faceColors=colours,
            smooth=False,
            drawEdges=True
        )

        self.mesh1.setGLOptions('additive')
        self.window.addItem(self.mesh1)

    def mesh(self):
        self.stream = sd.RawStream(
            samplerate=self.RATE,
            dtype=self.FORMAT,
            channels=self.CHANNELS,
            blocksize=self.CHUNK,
            )

        with self.stream:
            wf_data = self.stream.read(self.CHUNK)[0][:]

        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        wf_data = np.array(wf_data, dtype='int32') - 128
        wf_data = wf_data * 0.04
        wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        verts = np.array([
            [
                x, y, wf_data[xid][yid] * self.open_simplex.noise2d(x=xid / 5, y=yid / 5)
            ] for xid, x in enumerate(self.xpoints) for yid, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        r = self.startR
        g = self.startG
        b = self.startB

        faces = []
        colours = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces

            r += self.rStep
            g += self.gStep
            b += self.bStep
            col = [r, g, b, 1]

            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])

                colours.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.7])
                colours.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.7])

                # colours.append(col)
                # colours.append(col)

        faces = np.array(faces)
        colours = np.array(colours)

        return verts, faces, colours

    def update(self):
        verts, faces, colours = self.mesh()
        self.mesh1.setMeshData(
            vertexes=verts,
            faces=faces,
            faceColors=colours
        )


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec()

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.start()
        self.update()


if __name__ == '__main__':
    t = Terrain()
    t.animation()
