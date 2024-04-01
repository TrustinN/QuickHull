import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from utils import Facet
from utils import ConvexPoly
from rtree.r_tree_utils import NCube
from rtree.r_tree_utils import IndexRecord


class ConvexHull():
    def __init__(self, vertices, interior=[]):
        self.vertices = vertices
        self.interior = interior


def GetFacets(vertices):

    dim = len(vertices) - 1

    def helper(groups, num, b1, l):
        if num == 0:
            groups.append(l)
        else:
            for i in range(b1, dim + 1):
                new = l[:]
                new.append(vertices[i])
                helper(groups, num - 1, i + 1, new)

    groups = []
    helper(groups, dim, 0, [])
    return [Facet(g) for g in groups]


def HullInit(vertices):

    init_point = vertices[0]
    dim = len(init_point)
    hull_v = np.c_[init_point]
    rank = np.linalg.matrix_rank(hull_v)
    num_points = 1
    iter = 0

    while num_points < dim + 1:

        copy = hull_v.copy()
        copy = np.c_[copy, vertices[iter + 1] - init_point]
        new_rank = np.linalg.matrix_rank(copy)
        iter += 1

        if new_rank > rank:
            hull_v = copy
            rank = new_rank
            num_points += 1

    return hull_v


# returns vertices on the hull and the faces
def QuickHull(vertices):

    hull_v = HullInit(vertices).T
    facets = GetFacets(hull_v)

    return hull_v, facets


p1 = np.array([0, 0, 0])
p2 = np.array([np.cos(np.pi / 6), np.sin(np.pi / 6), 0])
p3 = np.array([np.cos(np.pi / 6), -np.sin(np.pi / 6), 0])
p4 = np.array([np.cos(np.pi / 6) / 2, 0, np.sin(np.pi / 3)])
p5 = np.array([.2, 0, .2])

vertices = [p1, p2, p3, p4]

v, f = QuickHull(vertices)
obs = ConvexPoly(faces=f, dim=3)
# obs.plot(ax)
# obs.animate(ax)
print(obs.tree)
obs.tree.Insert(IndexRecord(NCube.make_bound(p5), p5))
print(obs.contains_point(p5))
obs.tree.animate()









