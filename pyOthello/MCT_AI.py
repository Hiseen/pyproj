#Shengquan Ni 46564157 
import copy
import time
import random
import threading
from collections import defaultdict
import os.path
from ctypes import *
import cProfile

TRAIN_MODE='DEEP' #'WIDE'
TRAIN_TIMES={'WIDE':40,'DEEP':100,'NONE':0}

TRAIN_CURVE=lambda x:-2.8*x**2+2.8*x+0.3


class myThread(threading.Thread):  
    def __init__(self,turn,current_game,node):  
        threading.Thread.__init__(self)  
        self.turn=turn
        self.game=current_game
        self.node=node
          
    def run(self):
        for i in range(int(TRAIN_TIMES[TRAIN_MODE]*TRAIN_CURVE(self.game.get_stats()['.']/64))+random.randint(1,10)):
            self.node.MC_process(self.turn,copy.deepcopy(self.game))
        





class MCT_Node:
    def __init__(self,parent=None,win_rate=0.5,win=0,count=0):
        self.next_step=defaultdict(MCT_Node)
        self.parent=parent
        self.win_rate=win_rate
        self.win=win
        self.count=count

    @staticmethod
    def back_prop(node,game_result):
        while node:
            node.win+=game_result
            node.count+=1
            node.win_rate=float(node.win)/node.count
            node=node.parent


    def MC_process(self,turn,game):
        while not game.isover:
            game.drop(random.choice(game.vaildpos))
        self.back_prop(self,1 if turn==game.get_winner() else 0)

    def MCTS(self,current_game):
        if TRAIN_MODE!="NONE":
            threads=[]
            for i in current_game.vaildpos:
                if not self.next_step[i].parent:
                    self.next_step[i].parent=self
                temp=copy.deepcopy(current_game)
                turn=temp.turn
                temp.drop(i)
                t=myThread(turn,temp,self.next_step[i])
                t.start()
                threads.append(t)
            for i in threads:
                i.join()
        Max=-1
        result=None
        #print("----------------------------")
        if current_game.get_stats()['.']<36:
            return random.choice(current_game.vaildpos)
        for i in current_game.vaildpos:
            temp=self.next_step[i].win_rate
            #print("drop {}: winrate:{:.2f} count:{}".format(i,temp*100,self.next_step[i].count))
            if Max<temp:
                Max=temp
                result=i
        return result

    def get_next(self,next):
        if not self.next_step[next].parent:
            self.next_step[next].parent=self
        return self.next_step[next]

    def __str__(self):
        result='({:.4f},{},{})'.format(self.win_rate,self.win,self.count)
        if len(self.next_step)>0:
            result+="{"
            for i in self.next_step:
                result+='[{}]{};'.format(i,self.next_step[i])
            result=result[:-1]
            result+="}"
        return result
    def save(self,path="MCT_DATA.dat"):
        fp=open(path,'w')
        fp.write(str(self))
        fp.close()
        
    @staticmethod
    def load(path="MCT_DATA.dat"):
        if not os.path.exists(path):
            return None
        fp=open(path,'r')
        data=fp.read()
        fp.close()
        if data=='':
            return None
        t=data.find('{')
        values=eval(data[:t])
        root=MCT_Node(None,*values)
        #root.recursive_load(create_string_buffer(s,len(s)))
        root.highspeed_load(root,data[t+1:])
        return root


    def __eq__(self,other):
        result=self.win_rate==other.win_rate and self.win==other.win and self.count==self.count
        for i in self.next_step:
            if not other.next_step[i]==self.next_step[i]:
                return False
        return True

    @staticmethod
    def highspeed_load(self,data):
        i=0
        end=len(data)
        while i<end:
            f1=data.find(']',i)
            f2=data.find('{',i)
            f3=data.find(';',i)
            t1=data[i+2:f1-1].split(',')
            key=(int(t1[0]),int(t1[1]))
            if f2!=-1:
                if f3>f2:
                    t2=data[f1+2:f2-1].split(',')
                    self.next_step[key]=MCT_Node(self,float(t2[0]),int(t2[1]),int(t2[2]))
                    i=f2+1
                    self=self.next_step[key]
                else:
                    f4=data.find('}',i)
                    if f4>f3:
                        t2=data[f1+2:f3-1].split(',')
                        self.next_step[key]=MCT_Node(self,float(t2[0]),int(t2[1]),int(t2[2]))
                        i=f3+1
                    else:
                        t2=data[f1+2:f4-1].split(',')
                        self.next_step[key]=MCT_Node(self,float(t2[0]),int(t2[1]),int(t2[2]))
                        i=f4+1
                        self=self.parent
            else:
                f4=data.find('}',i)
                if f4<f3 or f3==-1:
                    t2=data[f1+2:f4-1].split(',')
                    self.next_step[key]=MCT_Node(self,float(t2[0]),int(t2[1]),int(t2[2]))
                    i=f4+1
                    self=self.parent
                else:
                    t2=data[f1+2:f3-1].split(',')
                    self.next_step[key]=MCT_Node(self,float(t2[0]),int(t2[1]),int(t2[2]))
                    if f4+1==end:
                        return None
                    i=f3+1
            while i<end and data[i] in (';','}'):
                if data[i]==';':
                    i+=1
                else:
                    i+=1
                    self=self.parent
        



if __name__=="__main__":
    a=MCT_Node.load()
    root=a
    while True:
        for i in a.next_step:
            print(i,a.next_step[i].win_rate,a.next_step[i].count)
        cmd=input().strip().lower()
        if cmd=="quit":
            break
        elif cmd=="reset":
            a=root
        elif cmd=="back":
            if a.parent!=None:
                a=a.parent
            else:
                print("the root state cannot back")
        else:
            try:
                pos=cmd.split(',')
                pos=tuple(map(lambda x:int(x),pos))
                assert(pos in a.next_step)
                a=a.get_next(pos)
            except:
                print("format error or the pos is not in next_step")
    














    
    
    
    
