import numpy as np
from colorutils import Color
import pyqtgraph as pg
import pyqtgraph.opengl as gl


class Facet():

    def __init__(self, vertices):

        self.vertices = vertices
        self.num_vertices = len(self.vertices)
        self.b = init_point = self.vertices[0]
        self.subspace = np.array([self.vertices[i + 1] - init_point for i in range(len(self.vertices) - 1)]).T
        self.dim = np.linalg.matrix_rank(self.subspace)
        self.o = np.array(self.vertices[:self.dim - 1])
        self.outside_vertices = []
        self.neighbors = []
        self.visited = False
        self.in_conv_poly = True
        self.rotate = np.array([[0, -1],
                                [1, 0]])
        self.triangles = []

        if self.num_vertices >= 0:
            if len(self.vertices[0]) == 2:
                n = np.dot(self.rotate, self.vertices[1] - self.vertices[0])
                self.normal = n / np.linalg.norm(n)

            elif self.num_vertices >= 3:
                v1 = self.vertices[1] - self.vertices[0]
                v2 = self.vertices[2] - self.vertices[0]
                n = np.cross(v1, v2)
                self.normal = n / np.linalg.norm(n)

    def add_neighbor(self, f):
        self.neighbors.append(f)

    def get_projection(self, p):
        approx = np.linalg.lstsq(self.subspace, p - self.b)[0]
        return p - (np.dot(self.subspace, approx) + self.b)

    def orient(self, p):
        return np.dot(self.normal, self.b - p)

    def plot(self, color, view):
        if self.dim == 1:
            line = pg.PlotDataItem(np.array([self.vertices[0],
                                             self.vertices[1]
                                             ]),
                                   connect="pairs", pen=pg.mkPen(color))
            self.p = line
            view.addItem(line)

        elif self.dim == 2:

            for t in self.triangles:
                md = gl.MeshData(vertexes=t, faces=np.array([[0, 1, 2]]))
                c = Color(web=color)
                rgb = c.rgb
                p0, p1, p2 = rgb[0], rgb[1], rgb[2]
                colors = np.ones((md.faceCount(), 4), dtype=float)
                colors[:, 3] = 0.3
                colors[:, 2] = np.linspace(p2/255, 1, colors.shape[0])
                colors[:, 1] = np.linspace(p1/255, 1, colors.shape[0])
                colors[:, 0] = np.linspace(p0/255, 1, colors.shape[0])

                md.setFaceColors(colors=colors)
                m1 = gl.GLMeshItem(meshdata=md, smooth=False, shader='shaded')
                m1.setGLOptions('additive')

                self.p = m1
                view.addItem(m1)

    def rm_plot(self, view):
        view.removeItem(self.p)

    def intersects_line(self, line, view):
        start = line[0]
        end = line[1]
        vec = end - start
        if np.sign(self.orient(start)) != np.sign(self.orient(end)):
            d = np.dot(self.normal, self.vertices[0])
            na = np.dot(self.normal, start)
            nv = np.dot(self.normal, vec)
            t = (d - na) / nv
            if 0 <= t <= 1:
                inter = t * vec + start
                p = gl.GLScatterPlotItem(pos=np.array([inter]))
                view.addItem(p)
                num = 0
                for fn in self.neighbors:
                    if fn.orient(inter) >= 0:
                        num += 1
                if num == len(self.neighbors):
                    return True
        return False


class ConvexPoly():

    def __init__(self, faces=[]):
        self.faces = faces
        if len(self.faces) > 0:
            f1 = self.faces[0]
            self.dim = f1.dim + 1
        copy = faces[:]
        for f in copy:
            if not f.in_conv_poly:
                self.faces.remove(f)

    def intersects_line(self, line):
        start = line[0]
        end = line[1]
        vec = end - start
        for f in self.faces:
            if np.sign(f.orient(start)) != np.sign(f.orient(end)):
                d = -np.dot(f.normal, f.vertices[0])
                na = np.dot(f.normal, start)
                nv = np.dot(f.normal, vec)
                t = (d - na) / nv
                inter = t * vec + start
                if -1 <= t <= 1:
                    inter = t * vec + start
                    num = 0
                    for fn in f.neighbors:
                        if fn.orient(inter) >= 0:
                            num += 1
                            print("Good")

                    if num == len(f.neighbors):
                        return True

        return False

    def contains_point(self, p):
        for f in self.faces:
            curr_face = f.vertices
            p2f = curr_face[0] - p
            n = f.normal
            d = np.dot(p2f, n) / np.linalg.norm(p2f)
            if d < 0:
                return False
        return True

    def plot(self, color, view):
        for f in self.faces:
            f.plot(color, view)






