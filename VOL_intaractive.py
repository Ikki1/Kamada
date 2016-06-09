import numpy as np
from matplotlib import pyplot as plt
from tkinter import *
import time

ep = 10**(-2)
global size
fullsize=500 #余白込みの画面のサイズ
size = 300 #画面のサイズ

edge= np.genfromtxt('edges-1.csv', delimiter=",").astype(np.int64)  #辺の情報
global N
N = np.max(edge).astype(np.int64)+1 #頂点の個数
global eN
eN = len(edge)  #辺の本数

fix = np.zeros(N)

#nodeの初期値
global node
node = np.zeros((N,2))
for i in range(N):
    node[i] = [(fullsize+size*np.cos(2*np.pi*i/N))*0.5, (fullsize+size*np.sin(2*np.pi*i/N))*0.5]

isConnect = np.zeros((N,N)) #繋がっている辺の組は1,繋がっていない組は0で表す
for i in range(eN):
    isConnect[edge[i][0]][edge[i][1]] = 1
    isConnect[edge[i][1]][edge[i][0]] = 1

#nodeの最短パスdを求める(Floyd法)
d = isConnect
for j in range(N):
    for i in range(N):
        if d[i][j] == 0:
            if i != j:
                d[i][j] = np.inf

for m in range(N):
    for i in range(N):
        for j in range(N):
            if d[i][m]+d[m][j]<d[i][j]:
                d[i][j] = d[i][m]+d[m][j] 

#ばねの自然長lを求める
l = size/np.max(d)*d


#kを求める
k = np.zeros((N,N)) #ばね定数
K = 1   #ばね定数の基準値
for j in range(N):
    for i in range(N):
        if i != j:
            k[i][j] = K/(d[i][j]**2)

            
root = Tk()

w = Canvas(root, width=fullsize, height=fullsize, bg='White')
w.pack()
back = w.create_rectangle(0, 0, fullsize, fullsize, fill='White', outline='White', tags = 'back')

circles = []
lines = []
texts = []
r=10
N=len(node)

#初期描画
for i in range(eN):
    lines.append(w.create_line(node[edge[i][0]][0], node[edge[i][0]][1], 
                           node[edge[i][1]][0], node[edge[i][1]][1], fill = 'Black', tags = 'edge'))

for i in range(N):
    circles.append(w.create_oval(node[i][0]-r, node[i][1]-r, node[i][0]+r, node[i][1]+r, fill="White", tags = 'node'))
    texts.append( w.create_text(node[i][0],node[i][1], text = str(i), fill='Black', tags = 'node'))


# 移動
def move_node(event):
    if val.get()==0:
        x = event.x
        y = event.y
        thisID = event.widget.find_withtag(CURRENT)[0]

        #circleをクリックしていた場合
        if (thisID-eN)%2 == 0: nodeID = int((thisID-eN-2)/2)

        #textをクリックしていた場合    
        else: nodeID = int((thisID-eN-3)/2)

        #nodeの更新
        node[nodeID] = [x,y]

        #circle,text,lineの更新(描画の更新)
        w.coords(circles[nodeID], x - r, y - r, x + r, y + r)
        w.coords(texts[nodeID], x, y)   
        for i in range(eN):
            if edge[i][0] == nodeID:
                w.coords(lines[i], x, y, node[edge[i][1]][0], node[edge[i][1]][1])
            if edge[i][1] == nodeID:
                w.coords(lines[i], node[edge[i][0]][0], node[edge[i][0]][1], x, y)
            
def click_edge(event):
    if val.get()==0:
        global x0, y0, edgeID, n0, n1
        x0 = event.x
        y0 = event.y
        thisID = event.widget.find_withtag(CURRENT)[0]
        edgeID = thisID - 2
        n0 = [node[edge[edgeID][0]][0],node[edge[edgeID][0]][1]]
        n1 = [node[edge[edgeID][1]][0],node[edge[edgeID][1]][1]]
            
def move_edge(event):
    if val.get()==0:
        x = event.x
        y = event.y

        #nodeの更新
        node[edge[edgeID][0]] = [n0[0] + x - x0, n0[1] + y - y0]
        node[edge[edgeID][1]] = [n1[0] + x - x0, n1[1] + y - y0]
        n0new = node[edge[edgeID][0]]
        n1new = node[edge[edgeID][1]]

        #circle,text,lineの更新(描画の更新)
        w.coords(circles[edge[edgeID][0]], n0new[0] - r, n0new[1] - r, n0new[0] + r, n0new[1] + r)
        w.coords(circles[edge[edgeID][1]], n1new[0] - r, n1new[1] - r, n1new[0] + r, n1new[1] + r)
        w.coords(texts[edge[edgeID][0]], n0new[0], n0new[1])
        w.coords(texts[edge[edgeID][1]], n1new[0], n1new[1])
        w.coords(lines[edgeID], n0new[0], n0new[1], n1new[0], n1new[1])
        for i in range(eN):
            if edge[i][0] == edge[edgeID][0] and i != edgeID:
                w.coords(lines[i], n0new[0], n0new[1], node[edge[i][1]][0], node[edge[i][1]][1])
            elif edge[i][1] == edge[edgeID][0] and i != edgeID:
                w.coords(lines[i], node[edge[i][0]][0], node[edge[i][0]][1], n0new[0], n0new[1])
            elif edge[i][0] == edge[edgeID][1] and i != edgeID:
                w.coords(lines[i], n1new[0], n1new[1], node[edge[i][1]][0], node[edge[i][1]][1])
            elif edge[i][1] == edge[edgeID][1] and i != edgeID:
                w.coords(lines[i], node[edge[i][0]][0], node[edge[i][0]][1], n1new[0], n1new[1])

def click_back(event):
    if val.get()==0:
        global x0_, y0_, nall
        x0_ = event.x
        y0_ = event.y
        nall=np.zeros((N,2))
        for i in range(N):
            nall[i] = [node[i][0],node[i][1]]
            
def move_back(event):
    if val.get()==0:
        x = event.x
        y = event.y

        #nodeの更新
        for i in range(N):
            node[i] = [nall[i][0] + x - x0_, nall[i][1] + y - y0_]

        #circle,text,lineの更新(描画の更新)
        for i in range(eN):
            w.coords(lines[i], node[edge[i][0]][0], node[edge[i][0]][1], node[edge[i][1]][0], node[edge[i][1]][1])
        for i in range(N):
            w.coords(circles[i], node[i][0]-r, node[i][1]-r, node[i][0]+r, node[i][1]+r)
            w.coords(texts[i], node[i][0],node[i][1])

def fix_node(event):
    if val.get()==0:
        thisID = event.widget.find_withtag(CURRENT)[0]

        #circleをクリックしていた場合
        if (thisID-eN)%2 == 0: nodeID = int((thisID-eN-2)/2)

        #textをクリックしていた場合    
        else: nodeID = int((thisID-eN-3)/2)

        if fix[nodeID] == 0:
            fix[nodeID] = 1
            w.itemconfigure(circles[nodeID], fill='Yellow')
        else:
            fix[nodeID] = 0
            w.itemconfigure(circles[nodeID], fill='White')

def move_graph():
    # バインディング
    w.tag_bind('node', '<Button1-Motion>', move_node)
    w.tag_bind('edge', '<1>', click_edge)
    w.tag_bind('edge', '<Button1-Motion>', move_edge)
    w.tag_bind('back', '<1>', click_back)
    w.tag_bind('back', '<Button1-Motion>', move_back)
    w.tag_bind('node', '<3>', fix_node)

def anime_graph():
    #dmを求める
    global node
    dm= np.zeros(N) #delta-m
    Ex= np.zeros(N) #Ex
    Ey= np.zeros(N) #Ey

    for m in range(N):
        for i in range(N):
            if m != i and fix[m] ==0:
                Ex[m]+= k[m][i]*(node[m][0]-node[i][0]-l[m][i]*(node[m][0]-node[i][0])
                                 /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
                Ey[m]+= k[m][i]*(node[m][1]-node[i][1]-l[m][i]*(node[m][1]-node[i][1])
                                 /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
    

    dm= (Ex**2+Ey**2)**(1/2)

    #dmが最大となるmを求める
    for i in range(N):
        if np.max(dm) == dm[i]:
            m = i

    while np.max(dm)>ep and val.get()==1:

        while dm[m]>ep and val.get()==1:

            #Ex,Ey,Exx,Exy,Eyyからdx,dyを求める
            Ex[m]= 0
            Ey[m]= 0
            Exx= 0 #Exx
            Exy= 0 #Exy, Eyx
            Eyy= 0 #Eyy

            for i in range(N):
                if m != i and fix[m] ==0:
                    Ex[m]+= k[m][i]*(node[m][0]-node[i][0]-l[m][i]*(node[m][0]-node[i][0])
                                     /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
                    Ey[m]+= k[m][i]*(node[m][1]-node[i][1]-l[m][i]*(node[m][1]-node[i][1])
                                     /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
                    Exx+= k[m][i]*(1-l[m][i]*(node[m][1]-node[i][1])**2
                                     /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(3/2)))
                    Exy+= k[m][i]*l[m][i]*(node[m][0]-node[i][0])*(node[m][1]-node[i][1])/(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(3/2))
                    Eyy+= k[m][i]*(1-l[m][i]*(node[m][0]-node[i][0])**2
                                     /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(3/2)))

            dx= (Ex[m]*Eyy-Ey[m]*Exy)/(Exy**2-Exx*Eyy) #dx
            dy= (Ey[m]*Exx-Ex[m]*Exy)/(Exy**2-Exx*Eyy) #dy

            #node,dmを更新
            node[m][0]+= dx
            node[m][1]+= dy
            dm[m]= (Ex[m]**2+Ey[m]**2)**(1/2)
            
            #描画の更新
            time.sleep(0.1)
            w.coords(circles[m], node[m][0] - r, node[m][1] - r, node[m][0] + r, node[m][1] + r)
            w.coords(texts[m], node[m][0], node[m][1])   
            for i in range(eN):
                if edge[i][0] == m:
                    w.coords(lines[i], node[m][0], node[m][1], node[edge[i][1]][0], node[edge[i][1]][1])
                if edge[i][1] == m:
                    w.coords(lines[i], node[edge[i][0]][0], node[edge[i][0]][1], node[m][0], node[m][1])
            w.pack() 
            w.update()

        #dmを求める
        dm= np.zeros(N) #delta-m
        Ex= np.zeros(N) #Ex
        Ey= np.zeros(N) #Ey

        for m in range(N):
            for i in range(N):
                if m != i and fix[m] ==0:
                    Ex[m]+= k[m][i]*(node[m][0]-node[i][0]-l[m][i]*(node[m][0]-node[i][0])
                                     /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
                    Ey[m]+= k[m][i]*(node[m][1]-node[i][1]-l[m][i]*(node[m][1]-node[i][1])
                                     /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))

        dm= (Ex**2+Ey**2)**(1/2)

        #dmが最大となるmを求める
        for i in range(N):
            if np.max(dm) == dm[i]:
                m = i


val = IntVar()
val.set(0)
move_graph()

r0 = Radiobutton(text = 'Drag / Stop', variable = val, value = 0, command = move_graph)
r0.pack()
r1 = Radiobutton(text = 'Animation', variable = val, value = 1, command = anime_graph)
r1.pack()

root.mainloop()