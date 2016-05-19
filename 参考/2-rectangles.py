import matplotlib.pyplot as plt

gca = plt.gca()

gca.add_patch(plt.Rectangle((10, 10), 20, 20, fc='r'))

plt.axis('scaled')
plt.show()