import matplotlib.pyplot as plt

gca = plt.gca()

circle = plt.Circle((0, 0), radius=0.75, fc='y')
gca.add_patch(circle)

plt.axis('scaled')
plt.show()