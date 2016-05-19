import matplotlib.pyplot as plt

gca = plt.gca()

gca.add_line(plt.Line2D((2, 8), (6, 6), lw=2.5))
gca.add_line(plt.Line2D((2, 8), (4, 4), lw=5, ls='-.', marker='.',
  markersize=50,
  markerfacecolor='r', markeredgecolor='r',
  alpha=0.5))

plt.axis('scaled')
plt.show()