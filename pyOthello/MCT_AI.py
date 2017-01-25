#Shengquan Ni 46564157 
import copy
import time
import random
import threading
from collections import defaultdict
import os.path

class myThread(threading.Thread):  
    def __init__(self,turn,current_game,node):  
        threading.Thread.__init__(self)  
        self.turn=turn
        self.game=current_game
        self.node=node
          
    def run(self):
        for i in range(random.randint(10,20)):
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
        threads=[]
        for i in current_game.vaildpos:
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
        for i in current_game.vaildpos:
            temp=self.next_step[i].win_rate
            #print("drop {}: winrate:{:.2f} count:{}".format(i,temp*100,self.next_step[i].count))
            if Max<temp:
                Max=temp
                result=i
        return result

    def get_next(self,next):
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
        root.recursive_load(data[t+1:])
        return root


    def __eq__(self,other):
        result=self.win_rate==other.win_rate and self.win==other.win and self.count==self.count
        for i in self.next_step:
            if not other.next_step[i]==self.next_step[i]:
                return False
        return True

    def recursive_load(self,data):
        while data:
            f1=data.find(']')
            f2=data.find('{')
            f3=data.find(';')
            key=eval(data[1:f1])
            if f2!=-1:
                if f3>f2:
                    self.next_step[key]=MCT_Node(None,*eval(data[f1+1:f2]))
                    data=self.next_step[key].recursive_load(data[f2+1:])
                    if data[0]==';':
                        data=data[1:]
                    elif data[0]=='}':
                        return data[1:]
                else:
                    f4=data.find('}')
                    if f4>f3:
                        self.next_step[key]=MCT_Node(None,*eval(data[f1+1:f3]))
                        data=data[f3+1:]
                    else:
                        self.next_step[key]=MCT_Node(None,*eval(data[f1+1:f4]))
                        return data[f4+1:]
            else:
                f4=data.find('}')
                if f4<f3 or f3==-1:
                    self.next_step[key]=MCT_Node(None,*eval(data[f1+1:f4]))
                    return data[f4+1:]
                else:
                    self.next_step[key]=MCT_Node(None,*eval(data[f1+1:f3]))
                    if f4+1==len(data):
                        return None
                    data=data[f3+1:]
        




    
    
    
