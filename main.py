import numpy as np
from utils import Facet
from utils import ConvexPoly
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
    hull_v = np.array([])
    rank = 0
    num_points = 0
    iter = 0

    while num_points < dim:

        copy = np.c_[vertices[iter + 1] - init_point]
        if rank != 0:
            copy = hull_v.copy()
            copy = np.c_[copy, vertices[iter + 1] - init_point]
        new_rank = np.linalg.matrix_rank(copy)
        iter += 1

        if new_rank > rank:
            hull_v = copy
            rank = new_rank
            num_points += 1

    return np.c_[init_point, hull_v]


# returns vertices on the hull and the faces
def QuickHull(vertices):

    hull_v = HullInit(vertices).T
    facets = GetFacets(hull_v)

    return hull_v, facets


def sample_point(bounds):
    rand_x = (bounds[1] - bounds[0]) * np.random.random_sample() + bounds[0]
    rand_y = (bounds[3] - bounds[2]) * np.random.random_sample() + bounds[2]
    rand_z = (bounds[5] - bounds[4]) * np.random.random_sample() + bounds[4]
    return rand_x, rand_y, rand_z


def insert(n, tree):

    points = []
    for i in range(n):
        x, y, z = sample_point([-1, 1, -1, 1, -1, 1])
        ti = np.array([x, y, z])
        points.append(ti)
        ir = IndexRecord(bound=None, tuple_identifier=ti)
        tree.Insert(ir)
    return points


p1 = np.array([-.5, -1, -.5])
p2 = np.array([np.cos(np.pi / 6), np.sin(np.pi / 6), 0])
p3 = np.array([np.cos(np.pi / 6), -np.sin(np.pi / 6), 0])
p4 = np.array([np.cos(np.pi / 6) / 2, 0, np.sin(np.pi / 3)])

vertices = [p1, p2, p3, p4]

v, f = QuickHull(vertices)
obs = ConvexPoly(faces=f, dim=3)

points = insert(150, obs.tree)

for p in points:
    if obs.contains_point(p):
        obs.tree.Delete(IndexRecord(bound=None, tuple_identifier=p))

obs.tree.animate()










