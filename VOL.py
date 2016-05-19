import numpy as np
import matplotlib.pyplot as plt

size = 10

edge= np.genfromtxt('edges-1.csv', delimiter=",").astype(np.int64)	#辺の情報

N = np.max(edge).astype(np.int64)+1	#頂点の個数
eN = len(edge)	#辺の本数

node = np.zeros((N,2))

for i in range(N):
    node[i] = [size/2*np.cos(2*np.pi*i/N),size/2*np.sin(2*np.pi*i/N)]

plt.figure(figsize=(size, size), dpi=80)

G1 = plt.gca()
plt.xlim(-size, size)
plt.ylim(-size, size)

c1 = plt.Circle((0, 0), radius=size/2, fill=False ,ls='-.')
G1.add_patch(c1)

for i in range(N):
    G1.add_patch(plt.Circle((node[i][0],node[i][1]), radius=0.1, fill=True, color = 'Black'))

for i in range(eN):
    G1.add_line(plt.Line2D((node[edge[i][0]][0], node[edge[i][1]][0]), 
    					   (node[edge[i][0]][1], node[edge[i][1]][1]), color = 'Black'))

plt.show()