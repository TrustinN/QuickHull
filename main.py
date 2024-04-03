import math
import numpy as np
from utils import Facet
from utils import ConvexPoly

np.random.seed(420)
# np.random.seed(720)


class ConvexHull():
    def __init__(self, vertices, interior=[]):
        self.vertices = vertices
        self.interior = interior


def CreateSimplex(vertices):
    dim = 0
    min_v, max_v = None, None
    hull = []
    while dim < 3:
        min, max = math.inf, -math.inf
        for v in vertices:
            val = v[dim]
            if val < min:
                min = val
                min_v = v
            elif val > max:
                max = val
                max_v = v
        if min != max:
            break
        dim += 1
    hull.append(min_v), hull.append(max_v)

    hyperplane = Facet(hull)
    closest_pt = None

    while True:
        closest_pt = None
        max_dist = -math.inf
        for v in vertices:
            dist = np.linalg.norm(hyperplane.get_projection(v))
            if dist > max_dist:
                max_dist = dist
                closest_pt = v

        if len(hull) == 3:
            break

        hull.append(closest_pt)
        hyperplane = Facet(hull)

    if hyperplane.orient(closest_pt) < 0:
        hull = hull[::-1]

    hull = [Facet(hull)] + [Facet([closest_pt, hull[(i + 1) % len(hull)], hull[i % len(hull)]]) for i in range(3)]
    return hull, 3


def AddToOutside(face, unclaimed):
    for i in range(len(unclaimed) - 1, -1, -1):
        v = unclaimed[i]
        if face.orient(v) < -0.005:
            unclaimed.pop(i)
            face.outside_vertices.append(v)


def CalculateHorizon(eyepoint, crossed_edge, start_idx, curr_face, horizon_edges, horizon_faces, unclaimed, visited, poly):

    if not curr_face.visited:

        if curr_face.orient(eyepoint) >= 0:
            horizon_faces.append(curr_face)
            horizon_edges.append(crossed_edge)

        else:
            visited.append(curr_face)
            curr_face.visited = True
            curr_face.in_conv_poly = False
            edges = curr_face.vertices
            unclaimed += curr_face.outside_vertices

            for i in range(len(edges)):
                cr_edge = [edges[(start_idx + i) % len(edges)], edges[(start_idx + i + 1) % len(edges)]]

                n = 0
                f = None
                cont = True
                st_idx = 0
                while cont:
                    f = curr_face.neighbors[n]

                    for j in range(len(f.vertices)):
                        l1 = [f.vertices[j], f.vertices[(j + 1) % len(f.vertices)]][::-1]
                        l2 = cr_edge
                        if np.array_equal(l1[0], l2[0]) and np.array_equal(l1[1], l2[1]):
                            st_idx = j
                            cont = False

                    n += 1

                CalculateHorizon(eyepoint, cr_edge, st_idx + 1, f, horizon_edges, horizon_faces, unclaimed, visited, poly)


# returns vertices on the hull and the faces
def QuickHull(vertices):

    hull, dim = CreateSimplex(vertices)
    for f in hull:
        AddToOutside(f, vertices)

    # Create convex hull which starts a tetrahedral
    conv = ConvexPoly()
    num_points = len(hull)
    for i in range(num_points):
        f = hull[i]
        conv.add_face(f)

        # connect faces as neighbors if they share an edge
        f.add_neighbor(hull[(i + 1) % num_points])
        f.add_neighbor(hull[(i + 2) % num_points])
        f.add_neighbor(hull[(i + 3) % num_points])

    unclaimed = []
    queue = [h for h in hull if len(h.outside_vertices) > 0]

    while queue:

        face = queue.pop()
        if face.in_conv_poly:

            max_dist = -math.inf
            farthest_pt = None

            for v in face.outside_vertices:
                curr_dist = np.linalg.norm(face.get_projection(v))

                if curr_dist > max_dist:
                    farthest_pt = v
                    max_dist = curr_dist

            horizon_edges, horizon_faces, visited = [], [], []
            CalculateHorizon(farthest_pt, None, 0, face, horizon_edges, horizon_faces, unclaimed, visited, conv)

            for f in visited:
                f.visited = False
                conv.tree.Delete(f)

            first_f = None
            prev_f = None
            for i in range(len(horizon_edges)):

                # Adding the cone
                ne = horizon_edges[i]
                ne.append(farthest_pt)
                f = Facet(ne)
                AddToOutside(f, unclaimed)

                if len(f.outside_vertices) > 0:
                    queue.append(f)
                conv.add_face(f)

                curr_hface = horizon_faces[i]
                curr_hface.add_neighbor(f)
                f.add_neighbor(curr_hface)
                if prev_f:
                    f.add_neighbor(prev_f)
                    prev_f.add_neighbor(f)

                prev_f = f

                if i == 0:
                    first_f = f

                elif i == len(horizon_edges) - 1:
                    f.add_neighbor(first_f)
                    first_f.add_neighbor(f)

                # Removing old neighbors
                n = 0
                cont = True
                while cont:
                    f = curr_hface.neighbors[n]

                    vert = f.vertices
                    for j in range(len(vert)):
                        l1 = [vert[j], vert[(j + 1) % len(f.vertices)]]
                        l2 = ne
                        if np.array_equal(l1[0], l2[0]) and np.array_equal(l1[1], l2[1]):
                            curr_hface.neighbors.pop(n)
                            cont = False
                    n += 1

    return conv


def sample_point(bounds):
    rand_x = (bounds[1] - bounds[0]) * np.random.random_sample() + bounds[0]
    rand_y = (bounds[3] - bounds[2]) * np.random.random_sample() + bounds[2]
    rand_z = (bounds[5] - bounds[4]) * np.random.random_sample() + bounds[4]
    return rand_x, rand_y, rand_z


def insert(n):

    points = []
    for i in range(n):
        x, y, z = sample_point([0, 1, -1, 1, 0, 1])
        ti = np.array([x, y, z])
        points.append(ti)
    return points


points = insert(500)
obs = QuickHull(points)
# for f in obs.faces:
#     obs.tree.Delete(f)

obs.tree.animate()

print("Done")









