import math
from cube import NCube
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Facet():

    def __init__(self, vertices):

        self.vertices = vertices
        self.num_vertices = len(self.vertices)
        bounds = list(map(lambda v: NCube([NCube.Endpoints(v[i], v[i]) for i in range(len(v))]), vertices))
        self.bound = NCube.combine(bounds)

    def plot(self, ax):
        ax.add_collection3d(Poly3DCollection([self.vertices], alpha=0.08))
        for v in self.vertices:
            ax.scatter(v[0], v[1], v[2], s=10, edgecolor='none')

    def plot_bound(self, ax):
        self.bound.plot(10, ax)


class Mesh():

    def __init__(self, faces):
        self.faces = faces
        bounds = [f.bound for f in faces]
        self.bound = NCube.combine(bounds)

    def plot(self, ax=None):
        for f in self.faces:
            f.plot(ax=ax)

    def plot_bound(self, ax):
        self.bound.plot(10, ax)

    def animate(self, ax):

        for angle in range(0, 1000, 1):

            ax.view_init(elev=angle + math.sin(1 / (angle + 1)) / 5, azim=.7 * angle, roll=.8 * angle)
            plt.draw()
            plt.pause(.001)

        plt.show()






