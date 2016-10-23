import random
from enum import Enum

#global functions:

def weighted_choice(weights):
    rnd = random.random() * 100
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
        

#global variables:
transition_rule={0:(-1,-1),1:(-1,0),2:(-1,1),3:(0,1),4:(1,1),5:(1,0),6:(1,-1),7:(0,-1)}
feedback_rate=1.2
decay_rate=0.9
signal_threshold=0.01
signal_type=Enum('singal_type','Free Target Search')

#classes definitions:
class Neuron:
    def __init__(self):
        self._weight=[12.5]*8
        
    def GetDirection(self,es):
        result=weighted_choice(self._weight)
        es._intensity*=decay_rate
        temp=self._weight[result]*(feedback_rate*es._intensity-1)
        for i in range(8):
            if i!=result:
                self._weight[i]-=temp/7
        self._weight[result]+=temp
        return transition_rule[result]

class ElectricSignal:
    def __init__(self,intensity=1,type=signal_type.Free):
        self._intensity=intensity
        assert type in signal_type
        self._type=type
        self.pos=[0,0]
        
    def IsDead(self):
        return self._intensity<signal_threshold
    
class Brain:
    def __init__(self,w,h):
        self._width=w
        self._height=h
        self._board=[[Neuron()for i in range(w)]for j in range(h)]
        self._signals=[]
        
    def Update(self):
        for i in self._signals:
            result=self._board[i.pos[1]][i.pos[0]].GetDirection(i)
            i.pos[0]+=result[0]
            i.pos[1]+=result[1]
            if i.pos[0]==-1:
                i.pos[0]=self._width-1
            elif i.pos[0]>=self._width:
                i.pos[0]=0
            if i.pos[1]==-1:
                i.pos[1]=self._height-1
            elif i.pos[1]>=self._height:
                i.pos[1]=0
        for i in range(len(self._signals)-1,-1,-1):
            if self._signals[i].IsDead():
                del i
        
    def AddSignal(self,es,posx=-1,posy=-1):
        if posx==-1:
            es.pos[0]=random.randint(0,self._width-1)
        else:
            es.pos[0]=posx
        if posy==-1:
            es.pos[1]=random.randint(0,self._height-1)
        else:
            es.pos[1]=posy
        self._signals.append(es)
    
        



if __name__=="__main__":
    count=0
    trash=[]
    def testfunc(brain,canvas):
        global count,trash
        while True:
            for i in trash:
                canvas.delete(i)
            if count==100:
                brain.AddSignal(ElectricSignal())
                count=0
            else:
                count+=1
            for i in brain._signals:
                left,top=i.pos[0]*cellsize,i.pos[1]*cellsize
                trash.append(canvas.create_rectangle(left,top,left+cellsize,top+cellsize,fill='black'))
            canvas.update()
            brain.Update()


    
    from tkinter import *
    window=Tk()
    width=50
    height=50
    cellsize=10
    window_height=height*cellsize
    window_width=width*cellsize
    brain=Brain(width,height)
    window.geometry('{}x{}'.format(window_width,window_height))
    canvas=Canvas(window,height=window_width,width=window_height)
    canvas.pack()
    for i in range(width):
        canvas.create_line(i*cellsize,0,i*cellsize,window_height)
    for i in range(height):
        canvas.create_line(0,i*cellsize,window_width,i*cellsize)
    testfunc(brain,canvas)
    window.mainloop()
       













