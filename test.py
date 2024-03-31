import numpy as np
from utils import Mesh
from utils import Facet
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f = plt.figure()
ax = f.add_subplot(1, 1, 1, projection=Axes3D.name)

p1 = np.array([0, 0, 0])
p2 = np.array([np.cos(np.pi / 6), np.sin(np.pi / 6), 0])
p3 = np.array([np.cos(np.pi / 6), -np.sin(np.pi / 6), 0])
p4 = np.array([np.cos(np.pi / 6) / 2, 0, np.sin(np.pi / 3)])

f1 = Facet(vertices=[p1, p2, p3])
f2 = Facet(vertices=[p1, p2, p4])
f3 = Facet(vertices=[p1, p3, p4])
f4 = Facet(vertices=[p2, p3, p4])

obs = Mesh(faces=[f1, f2, f3, f4])
# obs.plot_bound(ax)
obs.plot(ax)
obs.animate(ax)

print("Done!")



