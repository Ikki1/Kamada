import matplotlib.pyplot as plt

plt.axes()
gca = plt.gca()

circle = plt.Circle((0, 0), radius=10, fc='y')
gca.add_patch(circle)
gca.add_patch(plt.Rectangle((10, 10), 20, 20, fc='r'))

gca.add_line(plt.Line2D((2, 8), (6, 6), lw=2.5))
gca.add_line(plt.Line2D((2, 8), (4, 4), lw=5, ls='-.', marker='.',
  markersize=50,
  markerfacecolor='r', markeredgecolor='r',
  alpha=0.5))

gca.add_patch(plt.Polygon([[2, 1], [8, 1], [8, 4]]))
gca.add_patch(plt.Polygon([[2, 4], [2, 8], [4, 6], [6, 8]], closed=None, fill=None, edgecolor='r'))

plt.axis('scaled')
plt.show()
