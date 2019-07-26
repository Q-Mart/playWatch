# tutorial 4 (5th video)

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
from opensimplex import OpenSimplex

class Terrain(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.setGeometry(0, 100, 1920, 1080)
        self.w.show()
        self.w.setWindowTitle('Terrain')
        self.w.setCameraPosition(distance=30, elevation=8)

        # grid = gl.GLGridItem()
        # grid.scale(2, 2, 2)
        # self.w.addItem(grid)

        self.NSTEPS = 1
        self.ypoints = range(-20, 22, self.NSTEPS)
        self.xpoints = range(-20, 22, self.NSTEPS)
        self.nfaces = len(self.ypoints)
        self.offset = 0

        # Colours to match the ENSWBL asthetic
        self.startR = 95.2 / 255
        self.startG = 0.6 / 255
        self.startB = 59.9 / 255

        self.endR = 93.7 / 255
        self.endG = 58 / 255
        self.endB = 63.1 / 255

        self.rStep = (self.endR - self.startR) / 40
        self.gStep = (self.endG - self.startG) / 40
        self.bStep = (self.endB - self.startB) / 40

        self.open_simplex = OpenSimplex()

        verts = np.array([
            [
                x, y, 2.5 * self.open_simplex.noise2d(x=n / 5, y=m / 5)
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colours = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                colours.append([0,0,0,0])
                colours.append([0,0,0,0])

        faces = np.array(faces)
        colours = np.array(colours)
        self.mesh1 = gl.GLMeshItem(
            vertexes=verts,
            faces=faces,
            faceColors=colours,
            smooth=False,
            drawEdges=True
        )

        self.mesh1.setGLOptions('additive')
        self.w.addItem(self.mesh1)

    def update(self):
        verts = np.array([
            [
                x, y, 2.5 * self.open_simplex.noise2d(x=n / 5 + self.offset, y=m / 5 + self.offset)
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colours = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            col = [self.startR + self.rStep,
                   self.startG + self.gStep,
                   self.startB + self.bStep,
                   1]
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                # colours.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.7])
                # colours.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.7])


                colours.append(col)
                colours.append(col)

        faces = np.array(faces)
        colours = np.array(colours)

        self.mesh1.setMeshData(
            vertexes=verts,
            faces=faces,
            faceColors=colours
        )
        self.offset -= 0.01


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
