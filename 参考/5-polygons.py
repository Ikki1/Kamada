import matplotlib.pyplot as plt

gca = plt.gca()
#plt.axes()

gca.add_patch(plt.Polygon([[2, 1], [8, 1], [8, 4]]))
gca.add_patch(plt.Polygon([[2, 4], [2, 8], [4, 6], [6, 8]], closed=None, fill=None, edgecolor='r'))

plt.axis('scaled')
plt.show()