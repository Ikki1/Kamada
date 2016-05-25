import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ep = 10**(-3)
size = 10

edge= np.genfromtxt('edges-2.csv', delimiter=",").astype(np.int64)  #辺の情報

N = np.max(edge).astype(np.int64)+1 #頂点の個数
eN = len(edge)  #辺の本数

#nodeの初期値
node = np.zeros((N,2))
for i in range(N):
    node[i] = [size/2*np.cos(2*np.pi*i/N),size/2*np.sin(2*np.pi*i/N)]

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


#dmを求める
dm= np.zeros(N) #delta-m
Ex= np.zeros(N) #Ex
Ey= np.zeros(N) #Ey

for m in range(N):
    for i in range(N):
        if m != i:
            Ex[m]+= k[m][i]*(node[m][0]-node[i][0]-l[m][i]*(node[m][0]-node[i][0])
                             /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
            Ey[m]+= k[m][i]*(node[m][1]-node[i][1]-l[m][i]*(node[m][1]-node[i][1])
                             /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
        
dm= (Ex**2+Ey**2)**(1/2)

#dmが最大となるmを求める
for i in range(N):
    if np.max(dm) == dm[i]:
        m = i
        
while np.max(dm)>ep:
    
    while dm[m]>ep:
                
        #Ex,Ey,Exx,Exy,Eyyからdx,dyを求める
        Ex[m]= 0
        Ey[m]= 0
        Exx= 0 #Exx
        Exy= 0 #Exy, Eyx
        Eyy= 0 #Eyy
        
        for i in range(N):
            if m != i:
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
        
    #dmを求める
    dm= np.zeros(N) #delta-m
    Ex= np.zeros(N) #Ex
    Ey= np.zeros(N) #Ey

    for m in range(N):
        for i in range(N):
            if m != i:
                Ex[m]+= k[m][i]*(node[m][0]-node[i][0]-l[m][i]*(node[m][0]-node[i][0])
                                 /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))
                Ey[m]+= k[m][i]*(node[m][1]-node[i][1]-l[m][i]*(node[m][1]-node[i][1])
                                 /(((node[m][0]-node[i][0])**2+(node[m][1]-node[i][1])**2)**(1/2)))

    dm= (Ex**2+Ey**2)**(1/2)

    #dmが最大となるmを求める
    for i in range(N):
        if np.max(dm) == dm[i]:
            m = i

#グラフの位置の調整
mean= np.zeros(2)

for i in range(N):
    mean+=node[i]/N
    
node+= -mean

#描画
plt.figure(figsize=(size, size), dpi=80)

G1 = plt.gca()
plt.xlim(-size*0.6, size*0.6)
plt.ylim(-size*0.6, size*0.6)

c1 = plt.Circle((0, 0), radius=size/2, fill=False ,ls='-.')
G1.add_patch(c1)

for i in range(N):
    G1.add_patch(plt.Circle((node[i][0],node[i][1]), radius=0.3, fill=True, color = 'Black'))

for i in range(eN):
    G1.add_line(plt.Line2D((node[edge[i][0]][0], node[edge[i][1]][0]), 
                           (node[edge[i][0]][1], node[edge[i][1]][1]), color = 'Black'))

for i in range(N):
    G1.text(node[i][0],node[i][1],str(i),fontsize=20,horizontalalignment='center',verticalalignment='center',color='White',weight=1000)

plt.show()