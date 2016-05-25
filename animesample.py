import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure(figsize=(5, 5), dpi=80)
ax = plt.axes(xlim=(-3, 3), ylim=(-3, 3))

points = [[0,1],[1,0],[0,-1],[-1,0]]


#円
for i in range(len(points)):
    ax.add_patch(plt.Circle(points[i], 0.3, fc='c'))
#ラベル
for i in range(len(points)):
    ax.text(points[i][0],points[i][1], str(i))
#線
for i in range(len(points)):
    ax.add_line(plt.Line2D((points[i][0],points[(i+1)%4][0]),(points[i][1],points[(i+1)%4][1])))

#アニメーション
def animate(ai):
    for i in range(len(points)):
        points[i][0]= np.cos(np.radians(ai+90*i))
        points[i][1]= np.sin(np.radians(ai+90*i))


# Macで実行するときは blit=False に、その他の環境では blit=True にすること
anim = animation.FuncAnimation(fig, animate,  
                               frames=360, 
                               interval=20,
                               blit=False)

plt.show()