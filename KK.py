import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


ep = 10**(-3)
size = 10

edge= np.genfromtxt('edges-1.csv', delimiter=",").astype(np.int64)  #辺の情報

N = np.max(edge).astype(np.int64)+1 #頂点の個数
eN = len(edge)  #辺の本数

#nodeの初期値
node = np.zeros((N,2))
for i in range(N):
    node[i] = [size/2*np.cos(2*np.pi*i/N),size/2*np.sin(2*np.pi*i/N)]

#nodeの履歴を保存する
count = 0
save =[]
save.append(np.zeros((N,2)))
for i in range(N):
    save[count][i] = [node[i][0],node[i][1]]
count += 1

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
        
        #nodeの履歴を保存する
        save.append(np.zeros((N,2)))
        for i in range(N):
            save[count][i] = [node[i][0],node[i][1]]
        count += 1
        
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

#描画の設定
fig = plt.figure(figsize=(size, size), dpi=80)
ax = plt.axes(xlim=(-size*0.8, size*0.8), ylim=(-size*0.8, size*0.8))

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
    #描画
    #点
    for i in range(N):
        im.append(ax.add_patch(plt.Circle((save[t][i][0],save[t][i][1]), radius=0.3, fill=True, color = 'Black')))
    #辺
    for i in range(eN):
        im.append(ax.add_line(plt.Line2D((save[t][edge[i][0]][0], save[t][edge[i][1]][0]), 
                           (save[t][edge[i][0]][1], save[t][edge[i][1]][1]), color = 'Black')))
    #ラベル
    for i in range(N):
        im.append(ax.text(save[t][i][0],save[t][i][1],str(i),fontsize=16,horizontalalignment='center',verticalalignment='center',color='White',weight=1000))
    im.append(ax.text(-size*0.75,size*0.75,'frame: '+str(t),fontsize=16,color='Black',weight=500))
          

# アニメーション作成
anim = animation.FuncAnimation(fig, animate, fargs = (fig, im), 
        frames = len(save), interval = 100) 

# 表示

plt.show()