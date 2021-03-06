import numpy as np
from tkinter import *
import time
import sympy as sp
from itertools import product, chain

fullsize = 1000  # 余白込みの画面のサイズ
size = 300  # 画面のサイズ

ep = 0.01

dim = 3

#初期情報
edge = np.genfromtxt('edges-4.csv', delimiter=",").astype(np.int64)  # 辺の情報
N = np.max(edge).astype(np.int64) + 1  # 頂点の個数
eN = len(edge)  # 辺の本数

fix = np.zeros(N)

shapes = {
    'circles': [],
    'lines': [],
    'texts': []
}

def initializeNode():
    global node_pos, node_disp
    #論文の手法
    node_pos = np.random.rand(N, dim) * size
    node_pos -= (sum(node_pos) / N - np.ones(dim) * fullsize / 2)
    #今回用いた手法
    #thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
    #node_pos = (fullsize + size * np.c_[np.cos(thetas), np.sin(thetas), np.random.rand(N)]) * 0.5
    node_disp =np.zeros((N, dim))

initializeNode()

def springConstant():
    global k
    constant = 1  #定数の基準値
    k = constant * (size ** dim / N)**(1/dim)

springConstant()

def func_attractive(dist):
    length = 100
    return dist ** 2  / k

def func_repulsive(dist):
    return k ** 2 / dist

root = Tk()

def colors(r, g, b):
    c = '#' + ('%x' % int(r)).zfill(2) + ('%x' % int(g)).zfill(2) + ('%x' % int(b)).zfill(2)
    return c

color_num = 8

def colormap(i):
    maxcolor = np.array([255, 255, 255])
    mincolor = np.array([50, 50, 100])
    colorlist = np.array([np.linspace(maxcolor[i], mincolor[i], color_num, endpoint=True) for i in range(3)]).T
    return colors(colorlist[i][0], colorlist[i][1], colorlist[i][2])

def depth_to_color(z):
    num = int(z / (fullsize / color_num))
    if num <= 0: num = 0
    elif num >= color_num: num = color_num - 1
    return colormap(num)

def initializeDraw():
    #キャンパス
    global window, radius
    window = Canvas(root, width=fullsize, height=fullsize, bg='White')
    window.pack()
    back = window.create_rectangle(0, 0, fullsize, fullsize, fill='black', outline= '', tags='back')
    radius = 10

    # 初期描画
    for e in edge:
        shapes['lines'].append(window.create_line(node_pos[e[0]][0], node_pos[e[0]][1],
                                   node_pos[e[1]][0], node_pos[e[1]][1],
                                                  fill=depth_to_color((node_pos[e[0]][2] + node_pos[e[1]][2]) / 2), tags='edge'))

    for i in range(N):
        shapes['circles'].append(
            window.create_oval(node_pos[i][0] - radius, node_pos[i][1] - radius, node_pos[i][0] + radius, node_pos[i][1] + radius,
                          fill=depth_to_color(node_pos[i][2]), outline= '', tags='node_pos'))
        shapes['texts'].append(window.create_text(node_pos[i][0], node_pos[i][1], text=str(i), fill='Black', tags='node'))

initializeDraw()
    
# 移動
def move_node(event):
    if val.get() == 0:
        x = event.x
        y = event.y
        thisID = event.widget.find_withtag(CURRENT)[0]

        # circleをクリックしていた場合
        if (thisID - eN) % 2 == 0:
            nodeID = int((thisID - eN - 2) / 2)

        # textをクリックしていた場合
        else:
            nodeID = int((thisID - eN - 3) / 2)

        # nodeの更新
        node_pos[nodeID] = [x, y, node_pos[nodeID][2]]
        update_node(x, y, nodeID)


def update_node(x, y, nodeID):
    # circle,text,lineの更新(描画の更新)
    window.coords(shapes['circles'][nodeID], x - radius, y - radius, x + radius, y + radius)
    window.itemconfigure(shapes['circles'][nodeID], fill = depth_to_color(node_pos[nodeID][2]))
    window.coords(shapes['texts'][nodeID], x, y)
    for i in range(eN):
        if edge[i][0] == nodeID:
            window.coords(shapes['lines'][i], x, y, node_pos[edge[i][1]][0], node_pos[edge[i][1]][1])
        if edge[i][1] == nodeID:
            window.coords(shapes['lines'][i], node_pos[edge[i][0]][0], node_pos[edge[i][0]][1], x, y)
        window.itemconfigure(shapes['lines'][i], fill=depth_to_color((node_pos[edge[i][0]][2] + node_pos[edge[i][1]][2]) / 2))


def click_edge(event):
    if val.get() == 0:
        global x0, y0, edgeID, n0, n1
        x0 = event.x
        y0 = event.y
        thisID = event.widget.find_withtag(CURRENT)[0]
        edgeID = thisID - 2
        n0 = [node_pos[edge[edgeID][0]][0], node_pos[edge[edgeID][0]][1]]
        n1 = [node_pos[edge[edgeID][1]][0], node_pos[edge[edgeID][1]][1]]


def move_edge(event):
    if val.get() == 0:
        x = event.x
        y = event.y

        # nodeの更新
        node_pos[edge[edgeID][0]] = [n0[0] + x - x0, n0[1] + y - y0, node_pos[edge[edgeID][0]][2]]
        node_pos[edge[edgeID][1]] = [n1[0] + x - x0, n1[1] + y - y0, node_pos[edge[edgeID][1]][2]]
        n0new = node_pos[edge[edgeID][0]]
        n1new = node_pos[edge[edgeID][1]]

        # circle,text,lineの更新(描画の更新)
        update_node(n0new[0], n0new[1], edge[edgeID][0])
        update_node(n1new[0], n1new[1], edge[edgeID][1])


def click_back(event):
    if val.get() == 0:
        global x0_, y0_, nall
        x0_ = event.x
        y0_ = event.y
        nall = np.zeros((N, dim))
        for i in range(N):
            nall[i] = [node_pos[i][w] for w in range(dim)]


def move_back(event):
    if val.get() == 0:
        x = event.x
        y = event.y

        # nodeの更新
        for i in range(N):
            node_pos[i] = [nall[i][0] + x - x0_, nall[i][1] + y - y0_, node_pos[i][2]]
            update_node(node_pos[i][0], node_pos[i][1],i)


def fix_node(event):
    if val.get() == 0:
        thisID = event.widget.find_withtag(CURRENT)[0]

        # circleをクリックしていた場合
        if (thisID - eN) % 2 == 0:
            nodeID = int((thisID - eN - 2) / 2)

        # textをクリックしていた場合
        else:
            nodeID = int((thisID - eN - 3) / 2)

        fix[nodeID] = 1 - fix[nodeID]
        if fix[nodeID] == 1:
            window.itemconfigure(shapes['circles'][nodeID], outline='Yellow')
        else:
            window.itemconfigure(shapes['circles'][nodeID], outline='')


def move_graph():
    # バインディング
    window.tag_bind('node', '<Button1-Motion>', move_node)
    window.tag_bind('edge', '<1>', click_edge)
    window.tag_bind('edge', '<Button1-Motion>', move_edge)
    window.tag_bind('back', '<1>', click_back)
    window.tag_bind('back', '<Button1-Motion>', move_back)
    window.tag_bind('node', '<2>', fix_node)     #mac => <2>, windows => <3>


def distance(i, j):
    return np.linalg.norm(node_pos[i] - node_pos[j])

def delta(i, j):
    return node_pos[i] - node_pos[j]

def anime_graph():
    tempature = 1
    temp = 10
    active = True
    count = 0
    memo1 = np.ones((N, dim))
    memo2 = np.zeros((N, dim))

    while val.get() == 1:
        node_disp = np.zeros((N, dim))

        for i, j in product(range(N), range(N)):
            if i != j:
                node_disp[i] += delta(i, j) / distance(i, j) * func_repulsive(distance(i, j))

        for e in edge:
            attract = delta(e[0], e[1]) / distance(e[0], e[1]) * func_attractive(distance(e[0], e[1]))
            node_disp[e[0]] -= attract
            node_disp[e[1]] += attract

        time.sleep(0.01)

        for i in range(N):
            if fix[i] == 0:
                #論文の手法
                node_pos[i] += node_disp[i] / np.linalg.norm(node_disp[i]) * min(temp ** 2, np.linalg.norm(node_disp[i]))
                #今回用いた手法
                #node_pos[i] += node_disp[i] / np.linalg.norm(node_disp[i]) * tempature
                #node_pos[i] = [min(fullsize, max(0, node_pos[i][w])) for w in range(dim)]
            if count % 2 ==0 and active:
                memo2[i] = [node_pos[i][w] for w in range(dim)]

            # 描画の更新
            update_node(node_pos[i][0], node_pos[i][1], i)

        window.pack()
        window.update()

        if active and count % 2 == 0:
            if sum(sum(abs(memo1 - memo2))) < ep:
                print("nonactive")
                active = False
            else:
                memo1 = []
                memo1 += [[n[w] for w in range(dim)] for n in memo2]

        if active == False:
            tempature = max(tempature - 0.05, 0)

        temp = max(temp - 0.1, 0)

        count += 1


def rotation_3D():
    global node_pos
    node_pos -= (sum(node_pos) / N - np.ones(dim) * fullsize / 2)
    while dim == 3 and val.get() == 2:
        theta = np.pi / 360
        node_pos = (np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0],[- np.sin(theta), 0, np.cos(theta)]]).dot((node_pos - fullsize / 2).T)).T + fullsize / 2
        for i in range(N):
            update_node(node_pos[i][0], node_pos[i][1], i)

        time.sleep(0.01)

        window.pack()
        window.update()


def click_rotation(event):
    if dim == 3 and val.get() == 3:
        global x0, y0, nall
        x0 = event.x
        y0 = event.y
        nall = np.zeros((N, dim))
        for i in range(N):
            nall[i] = [node_pos[i][w] for w in range(dim)]

def move_rotation(event):
    global node_pos
    if dim == 3 and val.get() == 3:
        x = event.x
        y = event.y
        theta = - 2 * (x - x0) * np.pi / fullsize
        phi = 2 * (y - y0) * np.pi / fullsize
        rotation_theta = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [- np.sin(theta), 0, np.cos(theta)]])
        rotation_phi = np.array([[1, 0, 0], [0, np.cos(phi), - np.sin(phi)], [0, np.sin(phi), np.cos(phi)]])
        node_pos = ((rotation_phi.dot(rotation_theta)).dot((nall - fullsize / 2).T)).T + fullsize / 2

        for i in range(N):
            update_node(node_pos[i][0], node_pos[i][1], i)


def rotation_free():
    # バインディング
    window.tag_bind(ALL, '<1>', click_rotation)
    window.tag_bind(ALL, '<Button1-Motion>', move_rotation)


def button_command():
    global val
    val = IntVar()
    val.set(0)
    move_graph()

    r0 = Radiobutton(text='Drag / Stop', variable=val, value=0, command=move_graph)
    r0.pack()
    r1 = Radiobutton(text='Animation', variable=val, value=1, command=anime_graph)
    r1.pack()
    r2 = Radiobutton(text='3D View', variable=val, value=2, command=rotation_3D)
    r2.pack()
    r3 = Radiobutton(text='3D Drag', variable=val, value=3, command=rotation_free)
    r3.pack()


button_command()

root.mainloop()