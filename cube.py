import math
import numpy as np


class Bound:

    def __init__(self, dim):
        self.dim = dim

    def margin(self):
        return

    def expand(self):
        return

    def overlap(b1, b2):
        return

    def plot(self, c):
        return

    def rm_plot(self):
        return


class NCube(Bound):

    class Endpoints(tuple):

        def __new__(cls, *args):
            return super(NCube.Endpoints, cls).__new__(cls, tuple(args))

        def __init__(self, *args):
            self.length = self[1] - self[0]
            self.midpoint = (self[1] + self[0]) / 2

        def contains(self, other):
            if isinstance(other, tuple):
                return self[0] <= other[0] and self[1] >= other[1]
            else:
                return self[0] <= other <= self[1]

        def expand(e1, e2):
            return NCube.Endpoints(min(e1[0], e2[0]), max(e1[1], e2[1]))

        def dist_to(self, num):
            return min(abs(self[0] - num), abs(self[1] - num))

        def __str__(self):
            return f"({self[0]}, {self[1]})"

        def __repr__(self):
            return f"({self[0]}, {self[1]})"

    def __init__(self, bound=[]):

        self.bound = bound
        if bound:

            super().__init__(len(bound))
            self.p = None

            self.lengths = [b.length for b in bound]
            self.center = np.array([b.midpoint for b in bound])
            self.margin = self.dim * sum(self.lengths)
            self.vol = np.prod(self.lengths)

    def get_points(self):
        points = []

        def helper(points, curr_point, iter):
            if iter == self.dim:
                points.append(np.array(curr_point))

            else:
                for i in range(2):
                    helper(points, curr_point + [self.bound[iter][i]], iter + 1)

        helper(points, [], 0)
        return points

    def contains(self, other):

        for i in range(self.dim):
            if not self.bound[i].contains(other.bound[i]):
                return False

        return True

    def expand(b1, b2):
        return [NCube.Endpoints.expand(b1.bound[i], b2.bound[i]) for i in range(b1.dim)]

    def expand_vol(b1, b2):
        return np.prod([NCube.Endpoints.expand(b1.bound[i], b2.bound[i]).length for i in range(b1.dim)])

    def combine(bounds):
        nb = [NCube.Endpoints(math.inf, -math.inf) for i in range(bounds[0].dim)]
        for i in range(len(bounds)):
            curr_bound = bounds[i]
            nb = [NCube.Endpoints.expand(nb[j], curr_bound.bound[j]) for j in range(len(curr_bound.bound))]

        return NCube(nb)

    # returns overlap area of two bounds
    def overlap(self, other):

        overlaps = [.5 * (self.lengths[i] + other.lengths[i]) - abs(self.center[i] - other.center[i]) for i in range(self.dim)]
        prod = 1

        for o in overlaps:

            if o <= 0:
                return 0

            prod *= o

        return prod

    def get_dist(self, point):

        dist = np.array([self.bound[i].dist_to(point[i]) for i in range(self.dim)])
        btw = np.array([not self.bound[i].contains(point[i]) for i in range(self.dim)])
        rel_dist = dist[btw]

        if len(rel_dist) == 0:
            return 0

        return math.sqrt(sum(np.square(rel_dist)))

    def make_bound(point):
        return NCube([NCube.Endpoints(point[i], point[i]) for i in range(len(point))])

    def get_cube():

        phi = np.arange(1, 10, 2) * np.pi / 4
        Phi, Theta = np.meshgrid(phi, phi)

        x = np.cos(Phi) * np.sin(Theta)
        y = np.sin(Phi) * np.sin(Theta)
        z = np.cos(Theta) / np.sqrt(2)

        return x, y, z

    def plot(self, c, ax):

        if self.dim == 2:

            x = [self.bound[0][(i // 2) % self.dim] for i in range(2 * self.dim + 1)]
            y = [self.bound[1][(i // 2) % self.dim] for i in range(2 * (self.dim + 1))][1:]
            self.p = ax.plot(x, y, c=c, linewidth=.5)

        elif self.dim == 3:

            x, y, z = NCube.get_cube()
            self.p = ax.plot_surface(self.lengths[0] * x + self.center[0],
                                     self.lengths[1] * y + self.center[1],
                                     self.lengths[2] * z + self.center[2],
                                     alpha=0.08,
                                     shade=False,
                                     )

    def rm_plot(self):
        if self.dim == 2:
            if self.p:
                for handle in self.p:
                    handle.remove()
            self.p = None

        elif self.dim == 3:
            if self.p:
                self.p.remove()
            self.p = None

    def __str__(self):
        return f"{self.bound}"

    def __repr__(self):
        return f"{self.bound}"

