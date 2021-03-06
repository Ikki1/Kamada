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

global circlelabel 
circlelabel=""

class DraggableFigure:
    def __init__(self, circle):
        self.circle = circle
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.circle.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.circle.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.circle.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.circle.axes: return

        contains, attrd = self.circle.contains(event)
        if not contains: return
        x0, y0 = self.circle.center
        self.press = x0, y0, event.xdata, event.ydata
        global circlelabel
        circlelabel = self.circle.get_label

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        global lines
        global texts
        if self.press is None: return
        if event.inaxes != self.circle.axes: return
        if circlelabel == self.circle.get_label:
            x0, y0, xpress, ypress = self.press
            dx = event.xdata - xpress
            dy = event.ydata - ypress
            self.circle.center=(x0+dx,y0+dy)
            self.circle.figure.canvas.draw
            texts[int(circlelabel())].set_position((x0+dx,y0+dy))
            texts[int(circlelabel())].figure.canvas.draw()
            for i in range(eN):
                if str(edge[i][0]) ==circlelabel():
                    lines[i].set_xdata([x0+dx, lines[i].get_xdata()[1]])
                    lines[i].set_ydata([y0+dy, lines[i].get_ydata()[1]])
                    lines[i].figure.canvas.draw()
                if str(edge[i][1]) ==circlelabel():
                    lines[i].set_xdata([lines[i].get_xdata()[0], x0+dx])
                    lines[i].set_ydata([lines[i].get_ydata()[0], y0+dy])
                    lines[i].figure.canvas.draw()

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.circle.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.circle.figure.canvas.mpl_disconnect(self.cidpress)
        self.circle.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circle.figure.canvas.mpl_disconnect(self.cidmotion)

        
fig = plt.figure(figsize=(10, 10), dpi=80)
ax = plt.axes(xlim=(-8, 8), ylim=(-8, 8))

circles = []
lines = []
texts = []
for i in range(N):
    circles.append(ax.add_patch(plt.Circle(node[i], radius=0.3, fill=True, color = 'Black', label =str(i))))

for i in range(eN):
    lines.append(ax.add_line(plt.Line2D((node[edge[i][0]][0], node[edge[i][1]][0]), 
    					   (node[edge[i][0]][1], node[edge[i][1]][1]), color = 'Black',label =str(i))))

for i in range(N):
    texts.append(ax.text(node[i][0],node[i][1],str(i),fontsize=16,horizontalalignment='center',verticalalignment='center',color='White',weight=1000))

    
drs = []
for circle in circles:
    dr = DraggableFigure(circle)
    dr.connect()
    drs.append(dr)

plt.show()