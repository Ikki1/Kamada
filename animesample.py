import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

#描画の設定
fig = plt.figure(figsize=(5, 5), dpi=80)
ax = plt.axes(xlim=(-3, 3), ylim=(-3, 3))

points = [[0,1],[1,0],[0,-1],[-1,0]]

#フレームの内容を保持
im = [] 

#アニメ―ション
def animate(t, fig, im):

    #前回のフレーム内容を一旦削除
    if len(im) > 0:
        lenim=len(im)
        for i in range(lenim):
            im[lenim-(1+i)].remove()
            im.pop()
                    
    #描画のための計算
    for i in range(len(points)):
        points[i][0]= np.cos(np.radians(t+90*i))
        points[i][1]= np.sin(np.radians(t+90*i))
    #描画
    #線
    for i in range(len(points)):
        im.append(ax.add_line(plt.Line2D((points[i][0],points[(i+1)%4][0]),(points[i][1],points[(i+1)%4][1]))))
    #円
    for i in range(len(points)):
        im.append(ax.add_patch(plt.Circle(points[i], 0.3, fc='c')))
    #ラベル
    for i in range(len(points)):
        im.append(ax.text(points[i][0],points[i][1], str(i)))
        

# アニメーション作成
anim = animation.FuncAnimation(fig, animate, fargs = (fig, im), 
        frames = 360, interval = 20) 

# 表示
plt.show()