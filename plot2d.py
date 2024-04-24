import numpy as np
import math
import timeit
import pyqtgraph as pg
from hull import QuickHull

app = pg.mkQApp("QuickHull")
w = pg.plot().getViewBox()
w.show()
w.setWindowTitle('QuickHull')


radius = 20
center = np.array([0, 0])
vertices = []
for i in range(20):

    x_rand = radius * np.random.random_sample()
    y_rand = radius * np.random.random_sample()

    theta = np.random.random_sample() * 2 * math.pi
    p = np.array([x_rand * math.cos(theta),
                  y_rand * math.sin(theta),
                  ])

    vertices.append(p + center)

start = timeit.default_timer()
hull = QuickHull(vertices)
end = timeit.default_timer()
print(end - start)
print(hull.dim)

hull.plot(color="#05ff00", view=w)

pg.exec()


