import numpy as np
from tkinter import *
import time
import sympy as sp
from itertools import product, chain




#kk法の定数・変数
ep = 10 ** (-2)

#初期情報
edge = np.genfromtxt('edges-4.csv', delimiter=",").astype(np.int64)  # 辺の情報
N = np.max(edge).astype(np.int64) + 1  # 頂点の個数
eN = len(edge)  # 辺の本数

#インタラクション
fix = np.zeros(N)   # 固定するしないを記憶

fullsize = 500  # 余白込みの画面のサイズ
size = 300  # 画面のサイズ

shapes = {
    'circles': [],
    'lines': [],
    'texts': []
}

def initializeNode():
    global node
    thetas = np.linspace(0, 2 * np.pi, N, endpoint=False)
    node = (fullsize + size * np.c_[np.cos(thetas), np.sin(thetas)]) * 0.5

initializeNode()

def floydMethod():
    global distance
    distance = np.ones((N, N))*np.inf

    for e in edge:
        distance[e[0]][e[1]] = 1
        distance[e[1]][e[0]] = 1

    for m,i,j in product(range(N), range(N), range(N)):
        distance[i][j] = min(distance[i][m] + distance[m][j], distance[i][j])

floydMethod()

def springLength():
    global length
    length = size / np.max(distance) * distance

springLength()

def springConstant():
    global k
    K = 0.1  # ばね定数の基準値
    k = K / (distance ** 2) * (np.ones((N, N)) - np.diag(np.ones(N)))

springConstant()

root = Tk()

def initializeDraw():
    #キャンパス
    global window, radius
    window = Canvas(root, width=fullsize, height=fullsize, bg='White')
    window.pack()
    back = window.create_rectangle(0, 0, fullsize, fullsize, fill='White', outline='White', tags='back')
    radius = 10

    # 初期描画
    for e in edge:
        shapes['lines'].append(window.create_line(node[e[0]][0], node[e[0]][1],
                                   node[e[1]][0], node[e[1]][1], fill='Black', tags='edge'))

    for i in range(N):
        shapes['circles'].append(
            window.create_oval(node[i][0] - radius, node[i][1] - radius, node[i][0] + radius, node[i][1] + radius,
                          fill="White", tags='node'))
        shapes['texts'].append(window.create_text(node[i][0], node[i][1], text=str(i), fill='Black', tags='node'))

initializeDraw()

def differential():
    # sympy用の変数と方程式
    dim = 2
    p0, p1 = ['', '']
    for i in range(dim):
        p0 = p0 + ' p0' + str(i)
        p1 = p1 + ' p1' + str(i)
    symbols = sp.var('kij lij' + p0 + p1)
    lp0 = np.array(sp.var(p0))
    lp1 = np.array(sp.var(p1))
    norm = (np.sum((lp0 - lp1) ** 2)) ** (1 / 2)
    E = 1 / 2 * kij * (norm - lij) ** 2
    Eprime = [sp.diff(E, z) for z in list(lp0)]
    Ehess = [[sp.diff(E, z0, z1) for z0 in list(lp0)] for z1 in list(lp0)]
    global fEx,fEy, fExx, fExy, fEyx, fEyy
    fEx, fEy = [sp.lambdify(symbols, sp.simplify(s)) for s in Eprime]
    fExx, fExy, fEyx, fEyy = [sp.lambdify(symbols, sp.simplify(s)) for s in chain.from_iterable(Ehess)]

differential()

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
        node[nodeID] = [x, y]
        update_node(x, y, nodeID)


def update_node(x, y, nodeID):
    # circle,text,lineの更新(描画の更新)
    window.coords(shapes['circles'][nodeID], x - radius, y - radius, x + radius, y + radius)
    window.coords(shapes['texts'][nodeID], x, y)
    for i in range(eN):
        if edge[i][0] == nodeID:
            window.coords(shapes['lines'][i], x, y, node[edge[i][1]][0], node[edge[i][1]][1])
        if edge[i][1] == nodeID:
            window.coords(shapes['lines'][i], node[edge[i][0]][0], node[edge[i][0]][1], x, y)


def click_edge(event):
    if val.get() == 0:
        global x0, y0, edgeID, n0, n1
        x0 = event.x
        y0 = event.y
        thisID = event.widget.find_withtag(CURRENT)[0]
        edgeID = thisID - 2
        n0 = [node[edge[edgeID][0]][0], node[edge[edgeID][0]][1]]
        n1 = [node[edge[edgeID][1]][0], node[edge[edgeID][1]][1]]


def move_edge(event):
    if val.get() == 0:
        x = event.x
        y = event.y

        # nodeの更新
        node[edge[edgeID][0]] = [n0[0] + x - x0, n0[1] + y - y0]
        node[edge[edgeID][1]] = [n1[0] + x - x0, n1[1] + y - y0]
        n0new = node[edge[edgeID][0]]
        n1new = node[edge[edgeID][1]]

        # circle,text,lineの更新(描画の更新)
        update_node(n0new[0], n0new[1], edge[edgeID][0])
        update_node(n1new[0], n1new[1], edge[edgeID][1])


def click_back(event):
    if val.get() == 0:
        global x0_, y0_, nall
        x0_ = event.x
        y0_ = event.y
        nall = np.zeros((N, 2))
        for i in range(N):
            nall[i] = [node[i][0], node[i][1]]


def move_back(event):
    if val.get() == 0:
        x = event.x
        y = event.y

        # nodeの更新
        for i in range(N):
            node[i] = [nall[i][0] + x - x0_, nall[i][1] + y - y0_]
            update_node(node[i][0], node[i][1],i)   #edgeの更新回数的にはupdate_nodeを使うのは非効率ではある

        # # circle,text,lineの更新(描画の更新)
        # for i in range(eN):
        #     window.coords(lines[i], node[edge[i][0]][0], node[edge[i][0]][1], node[edge[i][1]][0], node[edge[i][1]][1])
        # for i in range(N):
        #     window.coords(circles[i], node[i][0] - radius, node[i][1] - radius, node[i][0] + radius, node[i][1] + radius)
        #     window.coords(texts[i], node[i][0], node[i][1])


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
            window.itemconfigure(shapes['circles'][nodeID], fill='Yellow')
        else:
            window.itemconfigure(shapes['circles'][nodeID], fill='White')


def move_graph():
    # バインディング
    window.tag_bind('node', '<Button1-Motion>', move_node)
    window.tag_bind('edge', '<1>', click_edge)
    window.tag_bind('edge', '<Button1-Motion>', move_edge)
    window.tag_bind('back', '<1>', click_back)
    window.tag_bind('back', '<Button1-Motion>', move_back)
    window.tag_bind('node', '<2>', fix_node)     #mac => <2>, windows => <3>


def anime_graph():
    # dmを求める
    global node
    delta = np.zeros(N)  # delta-m
    Ex = np.zeros(N)  # Ex
    Ey = np.zeros(N)  # Ey

    for m,i in product(range(N), range(N)):
        if m != i and fix[m] == 0:
            Ex[m] += fEx(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])
            Ey[m] += fEy(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])

    delta = (Ex ** 2 + Ey ** 2) ** (1 / 2)

    # dmが最大となるmを求める
    for i in range(N):
        if np.max(delta) == delta[i]:
            m = i

    while np.max(delta) > ep and val.get() == 1:

        while delta[m] > ep and val.get() == 1:

            # Ex,Ey,Exx,Exy,Eyyからdx,dyを求める
            Ex[m] = 0
            Ey[m] = 0
            Exx = 0  # Exx
            Exy = 0  # Exy, Eyx
            Eyy = 0  # Eyy

            for i in range(N):
                if m != i and fix[m] == 0:
                    Ex[m] += fEx(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])
                    Ey[m] += fEy(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])
                    Exx += fExx(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])
                    Exy += fExy(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])
                    Eyy += fEyy(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])

            dx = (Ex[m] * Eyy - Ey[m] * Exy) / (Exy ** 2 - Exx * Eyy)  # dx
            dy = (Ey[m] * Exx - Ex[m] * Exy) / (Exy ** 2 - Exx * Eyy)  # dy

            # node,dmを更新
            node[m][0] += dx
            node[m][1] += dy
            delta[m] = (Ex[m] ** 2 + Ey[m] ** 2) ** (1 / 2)

            # 描画の更新
            time.sleep(0.1)
            update_node(node[m][0], node[m][1], m)
            window.pack()
            window.update()

        # dmを求める
        delta = np.zeros(N)  # delta-m
        Ex = np.zeros(N)  # Ex
        Ey = np.zeros(N)  # Ey

        for m in range(N):
            for i in range(N):
                if m != i and fix[m] == 0:
                    Ex[m] += fEx(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])
                    Ey[m] += fEy(k[m][i], length[m][i], node[m][0], node[m][1], node[i][0], node[i][1])

        delta = (Ex ** 2 + Ey ** 2) ** (1 / 2)

        # dmが最大となるmを求める
        for i in range(N):
            if np.max(delta) == delta[i]:
                m = i

def button_command():
    global val
    val = IntVar()
    val.set(0)
    move_graph()

    r0 = Radiobutton(text='Drag / Stop', variable=val, value=0, command=move_graph)
    r0.pack()
    r1 = Radiobutton(text='Animation', variable=val, value=1, command=anime_graph)
    r1.pack()

button_command()

root.mainloop()