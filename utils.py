import math
import numpy as np
from rtree.r_tree_utils import NCube
from rtree.r_tree_utils import IndexRecord
from rtree.r_star_tree import RTree
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Graph():
    def __init__(self, vertices=[]):
        self.vertices = vertices

    def add_vertex(self, v):
        self.vertices.append(v)


class Facet(IndexRecord):

    def __init__(self, vertices):

        self.vertices = vertices
        self.num_vertices = len(self.vertices)
        bounds = list(map(lambda v: NCube([NCube.Endpoints(v[i], v[i]) for i in range(len(v))]), vertices))
        self.bound = NCube.combine(bounds)
        self.b = init_point = self.vertices[0]
        self.subspace = np.array([self.vertices[i + 1] - init_point for i in range(len(self.vertices) - 1)]).T
        self.dim = np.linalg.matrix_rank(self.subspace) + 1
        self.o = np.array(self.vertices[:self.dim])
        self.outside_vertices = []
        self.neighbors = []
        self.visited = False
        self.in_conv_poly = True

    def add_neighbor(self, f):
        self.neighbors.append(f)

    def plot(self, color, ax):
        self.plots = [ax.add_collection3d(Poly3DCollection([self.vertices], alpha=0.08))]
        for v in self.vertices:
            self.plots.append(ax.scatter(v[0], v[1], v[2], c=color, s=10, edgecolor='none'))

    def rm_plot(self):
        for p in self.plots:
            p.remove()

    def normal(self):
        v1 = self.vertices[1] - self.vertices[0]
        v2 = self.vertices[2] - self.vertices[0]
        n = np.cross(v1, v2)
        return n / np.linalg.norm(n)

    def get_projection(self, p):
        approx = np.linalg.lstsq(self.subspace, p - self.b)[0]
        return p - (np.dot(self.subspace, approx) + self.b)

    def orient(self, p):
        c1 = np.vstack([self.o, p])
        c2 = np.c_[c1, np.ones(self.dim + 1)]
        return np.linalg.det(c2)

    def plot_bound(self, ax):
        self.bound.plot(10, ax)

    def __eq__(self, other):
        if isinstance(other, Facet):
            for i in range(len(self.vertices)):
                if not np.array_equal(self.vertices[i], other.vertices[i]):
                    return False
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return f"val: {self.vertices}"

    def __repr__(self):
        return f"val: {self.vertices}"


class ConvexPoly():

    def __init__(self, faces=[]):

        self.faces = faces
        for f in faces:
            self.add_face(f)

        self.tree = RTree(5, dim=3, plotting=True)
        self.graph = Graph()

    def add_face(self, face):
        self.faces.append(face)
        self.tree.Insert(face)
        self.graph.add_vertex(face)

    def contains_point(self, p):
        for f in self.faces:
            curr_face = f.vertices
            p2f = curr_face[0] - p
            n = f.normal()
            d = np.dot(p2f, n) / np.linalg.norm(p2f)
            if d < 0:
                return False
        return True

    def plot(self, ax=None):
        for f in self.faces:
            f.plot(ax=ax)

    def animate(self, ax):

        for angle in range(0, 1000, 1):

            ax.view_init(elev=angle + math.sin(1 / (angle + 1)) / 5, azim=.7 * angle, roll=.8 * angle)
            plt.draw()
            plt.pause(.001)

        plt.show()







