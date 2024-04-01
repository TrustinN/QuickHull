import math
import numpy as np
from rtree.r_tree_utils import NCube
from rtree.r_tree_utils import IndexRecord
from rtree.r_star_tree import RTree
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Facet(IndexRecord):

    def __init__(self, vertices):

        self.vertices = vertices
        self.num_vertices = len(self.vertices)
        bounds = list(map(lambda v: NCube([NCube.Endpoints(v[i], v[i]) for i in range(len(v))]), vertices))
        self.bound = NCube.combine(bounds)
        self.b = init_point = self.vertices[0]
        self.subspace = np.array([self.vertices[i + 1] - init_point for i in range(len(self.vertices) - 1)]).T

    def plot(self, color, ax):
        ax.add_collection3d(Poly3DCollection([self.vertices], alpha=0.08))
        plots = []
        for v in self.vertices:
            plots.append(ax.scatter(v[0], v[1], v[2], c=color, s=10, edgecolor='none'))
        return plots

    def get_projection(self, p):
        approx = np.linalg.lstsq(self.subspace, p - self.b)[0]
        return p - (np.dot(self.subspace, approx) + self.b)

    def plot_bound(self, ax):
        self.bound.plot(10, ax)

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __str__(self):
        return f"val: {self.vertices}"

    def __repr__(self):
        return f"val: {self.vertices}"


class RayCast():
    def __init__(self, tree, p):
        self.inside = False
        self.tree = tree

        def contains_point(p):

            def helper(node):
                axis_aligned = True
                if isinstance(node, RTree.LeafNode):
                    for n in node.items:
                        if type(n) is Facet:
                            proj = n.get_projection(p)
                            if proj[0] < 0:
                                self.inside = not self.inside

                else:
                    for i in range(len(p) - 1):
                        interval = node.covering.bound[i + 1]
                        axis_aligned = interval[0] <= p[i + 1] <= interval[1] and axis_aligned
                    if axis_aligned:
                        for b in node.items:
                            helper(b.pointer)

            helper(self.tree.root)
            return self.inside

        self.contains = contains_point(p)


class ConvexPoly():

    def __init__(self, faces, dim):

        self.faces = faces
        self.tree = RTree(5, dim=dim, plotting=True)
        for f in self.faces:
            self.tree.Insert(f)

    def contains_point(self, p):
        rc = RayCast(self.tree, p)
        return rc.contains

    def plot(self, ax=None):
        for f in self.faces:
            f.plot(ax=ax)

    def animate(self, ax):

        for angle in range(0, 1000, 1):

            ax.view_init(elev=angle + math.sin(1 / (angle + 1)) / 5, azim=.7 * angle, roll=.8 * angle)
            plt.draw()
            plt.pause(.001)

        plt.show()






