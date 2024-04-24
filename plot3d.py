import numpy as np
import math
import timeit
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from hull import QuickHull
from PyQt6.QtGui import QVector3D

# np.random.seed(1000)
np.random.seed(1200)
app = pg.mkQApp("QuickHull")
view = gl.GLViewWidget()
view.show()
view.setWindowTitle('QuickHull')

view.setCameraPosition(QVector3D(500, 0, 200), distance=1000)

g = gl.GLGridItem()
g.translate(400, 400, -200)
g.scale(100, 100, 100)
view.addItem(g)

x = np.array([100, 0, 0])
y = np.array([0, 100, 0])
z = np.array([0, 0, 100])
origin = np.array([0, 0, 0])

line = gl.GLLinePlotItem(pos=np.array([x, origin]), color=pg.mkColor("#ff0000"))
view.addItem(line)

line = gl.GLLinePlotItem(pos=np.array([y, origin]), color=pg.mkColor("#00ff00"))
view.addItem(line)

line = gl.GLLinePlotItem(pos=np.array([z, origin]), color=pg.mkColor("#0000ff"))
view.addItem(line)

# radius = 500
# center = np.array([400, 0, 200])
# vertices = []
# for i in range(16):
#
#     x_rand = radius * np.random.random_sample()
#     y_rand = radius * np.random.random_sample()
#     z_rand = radius * np.random.random_sample()
#
#     theta = np.random.random_sample() * 2 * math.pi
#     phi = np.random.random_sample() * math.pi
#     p = np.array([x_rand * math.cos(phi) * math.sin(theta),
#                   y_rand * math.sin(phi) * math.sin(theta),
#                   z_rand * math.cos(theta),
#                   ])
#
#     vertices.append(p + center)
#
# start = timeit.default_timer()
# hull = QuickHull(vertices)
# end = timeit.default_timer()
#
# hull.plot(color="#05ff00", view=view)

unit = 1000
grid_length = 1000 / 3
length = grid_length / 6

min_x = grid_length - length / 2
max_x = grid_length + length / 2

min_y = 0
max_y = grid_length

min_z = 0
max_z = grid_length

points = gl.GLScatterPlotItem(pos=np.array([np.array([min_x, min_y, min_z]),
                                            np.array([max_x, min_y, min_z]),
                                            np.array([min_x, max_y, min_z]),
                                            np.array([min_x, min_y, max_z]),
                                            np.array([max_x, max_y, min_z]),
                                            np.array([max_x, min_y, max_z]),
                                            np.array([min_x, max_y, max_z]),
                                            np.array([max_x, max_y, max_z]),
                                            ]))
view.addItem(points)

wall = QuickHull([np.array([min_x - 1, min_y, min_z]),
                  np.array([max_x, min_y, min_z]),
                  np.array([min_x - 1, max_y, min_z]),
                  np.array([min_x, min_y, max_z]),
                  np.array([max_x, max_y, min_z]),
                  np.array([max_x, min_y, max_z]),
                  np.array([min_x, max_y, max_z]),
                  np.array([max_x, max_y, max_z]),
                  ])

start_pos = np.array([grid_length / 2 for i in range(3)])
end_pos = np.array([grid_length, grid_length / 2, grid_length / 2])
line = gl.GLLinePlotItem(pos=np.array([start_pos, end_pos]))
view.addItem(line)
wall.faces[3].plot(color="#05ff00", view=view)
print(wall.faces[3].intersects_line([start_pos, end_pos], view))



pg.exec()
















