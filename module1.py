# -*- coding: utf-8 -*-
lengthofchessbox=8
gapsize=40
chesssize=gapsize*0.4
SCREEN_SIZE=(gapsize*(lengthofchessbox+3),gapsize*(lengthofchessbox+3))
count0=0
count1=0
count2=0
MAX_VALUE=10000000
std_depth=3
rounds=0
import pygame
import random
import time
import copy
import math
import os
import sys

def P_list(p):
    for i in p:
        print(i)

'''
import ctypes   
whnd = ctypes.windll.kernel32.GetConsoleWindow()   
if whnd != 0:   
    ctypes.windll.user32.ShowWindow(whnd, 0)   
    ctypes.windll.kernel32.CloseHandle(whnd) 
'''

def can_turn_chess(list,dx,dy,flag,startx,starty):
    x=startx+dx
    y=starty+dy
    reverse=False
    step=0
    oppchess=False
    while(x<lengthofchessbox and x>=0 and y<lengthofchessbox and y>=0):
        if list[x][y]==0:
            return (False,0,x,y)
        elif list[x][y]==-flag:
             oppchess=True
        elif list[x][y]==flag:
            if oppchess==False:
                break
            else:
                return (True,step,x,y)
        step+=1
        x+=dx
        y+=dy
    return(False,0,0,0)





def turn_chess(list,dx,dy,flag,startx,starty):
    res,step,x,y=can_turn_chess(list,dx,dy,flag,startx,starty)
    if res:
        for i in range(step):
            x-=dx
            y-=dy
            list[x][y]=flag



def make_putpos(chesses,flag):
    list=[]
    for i in range(lengthofchessbox):
        for j in range(lengthofchessbox):
            if chesses[j][i]==0:
                for k in range(8):
                    if switch2[k](flag,j,i)[0]:
                        list.append((j,i))
                        break
    return list

def can_move(chesses,flag):
     for i in range(lengthofchessbox):
        for j in range(lengthofchessbox):
            if chesses[i][j]==0:
                for k in range(8):
                    if switch2[k](flag,i,j)[0]:
                        return True
     return False


def rules(flag,x,y):
    global needrefresh, player, lengthofchessbox, chesses, gameover,canputchesspos,count0,count1,count2,AI
    needrefresh=True
    for i in range(8):
        switch[i](chesses,flag,x,y)
    gameover=True
    flag=1 if player else -1
    vaildpos=False
    for i in range(lengthofchessbox):
        for j in range(lengthofchessbox):
            if chesses[i][j]==0:
                for k in range(8):
                    if switch2[k](flag,i,j)[0]:
                        vaildpos=True
                        canputchesspos.append((i,j))
                        break
    gameover=not vaildpos
    if gameover:
        del canputchesspos[:]
        player=not player
        AI= not AI
        flag=1 if player else -1
    vaildpos=False
    for i in range(lengthofchessbox):
        for j in range(lengthofchessbox):
            if chesses[i][j]==0:
                for k in range(8):
                    if switch2[k](flag,i,j)[0]:
                        vaildpos=True
                        canputchesspos.append((i,j))
                        break
    gameover=not vaildpos
    count0=0
    count1=0
    count2=0
    for i in range(lengthofchessbox):
        for j in range(lengthofchessbox):
            if chesses[i][j]==0:
                count0+=1
            elif chesses[i][j]==1:
                count1+=1
            else:
                count2+=1
    if count0==0 or count1==0 or count2==0:
         gameover=True 


def evaluate(chess,flag,step):
    res1=0
    res2=0
    res3=0
    res4=0
    countours=0
    countopps=0
    #静态矩阵估值：
    #稳定点估值：
    #行动力估值：
    for i in range(lengthofchessbox):
           for j in range(lengthofchessbox):
               if chess[i][j]==flag:
                   res1+=values[i][j]
                   countours+=1
               elif chess[i][j]==-flag:
                   res1-=values[i][j]
                   countopps+=1
    if step>=56:
        res3=(countours-countopps)*10
    else:
        res2+=chess[0][0]+chess[0][lengthofchessbox-1]+chess[lengthofchessbox-1][0]+chess[lengthofchessbox-1][lengthofchessbox-1]-(chess[1][1]+chess[1][lengthofchessbox-2]+chess[lengthofchessbox-2][1]+chess[lengthofchessbox-2][lengthofchessbox-2])*flag*20
    if step>16 and step<48:
        res4+=len(make_putpos(chess,flag))
        res4-=len(make_putpos(chess,-flag))
    res1=res1*((64-step)/32)
    res2=res2*(step/20)
    res3=res3*((step-55)/2)
    res4*=5
    #print('矩阵:',,'稳定点:',flag*,'棋子差:',flag*res3*((step-55)/4),'行动力:',flag*res4*5,'total',flag*(res1*((64-step)/32)+res2*((step)/28)+res3*((step-56)/4)+res4*5))
    return res1+res2+res3+res4
    











def calc_value(chess,a,b,flag,depth,max_depth,step):
    if depth>=max_depth or (can_move(chess,flag) is False and can_move(chess,-flag) is False):
        res=flag*evaluate(chess,flag,step-depth)
        #sys.stdout.write(str(bin(abs(int(res))))[2:])
        #sys.stdout.flush()
        return res
    max=-MAX_VALUE
    pos=make_putpos(chess,flag)
    if depth==0:
        res=[pos[0][0],pos[0][1]]
    for i in pos:
        newchess=copy.deepcopy(chess)
        newchess[i[0]][i[1]]=flag
        if depth==0:
            print('-----------------------------------')
        print('当前选择落子点:',i)
        for j in range(8):
            switch[j](newchess,flag,i[0],i[1])
        val=-calc_value(newchess,-b,-a,-flag,depth+1,max_depth,step)
        if val>a:
            a=val
            if depth==0:
                res=[i[0],i[1]]
            if val>=b:
                if depth==0:
                    print('最终得分',val)
                    print('选择落子点',res[0],res[1])
                return res if depth==0 else val
        max=val if val>max else max
    if depth==0:
        print('最终得分',max)
        print('选择落子点',res[0],res[1])
    else:
        print('当前得分',max)
    return res if depth==0 else max



        



from pygame.locals import *
from sys import exit
pygame.init()
screen=pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.display.set_caption("wow")
time1=pygame.time.Clock()
needrefresh=True
#chess
chesses=[[0 for i in range(lengthofchessbox)] for j in range(lengthofchessbox)]
chesses[int(lengthofchessbox/2)][int(lengthofchessbox/2)]=-1
chesses[int(lengthofchessbox/2)-1][int(lengthofchessbox/2)-1]=-1
chesses[int(lengthofchessbox/2)][int(lengthofchessbox/2)-1]=1
chesses[int(lengthofchessbox/2)-1][int(lengthofchessbox/2)]=1
#PVE?
AI=False
#估值矩阵:
values=[
    [120 ,-90,30 ,30 ,30 ,30 ,-90,120 ],
    [-90,-100,5  ,5  ,5  ,5  ,-100,-90],
    [30 ,5  ,1  ,1  ,1  ,1  ,5  ,30 ],
    [30 ,5  ,1  ,1  ,1  ,1  ,5  ,30 ],
    [30 ,5  ,1  ,1  ,1  ,1  ,5  ,30 ],
    [30 ,5  ,1  ,1  ,1  ,1  ,5  ,30 ],
    [-90,-100,5  ,5  ,5  ,5  ,-100,-90],
    [120 ,-90,30 ,30 ,30 ,30 ,-90,120 ]]
#player
player=True #True->black False->white
gameover=False
canputchesspos=[]
font=pygame.font.SysFont('system',16)
#switch
switch2={
    0:lambda flag,x,y:can_turn_chess(chesses,0,1,flag,x,y),
    1:lambda flag,x,y:can_turn_chess(chesses,1,1,flag,x,y),
    2:lambda flag,x,y:can_turn_chess(chesses,1,0,flag,x,y),
    3:lambda flag,x,y:can_turn_chess(chesses,0,-1,flag,x,y),
    4:lambda flag,x,y:can_turn_chess(chesses,-1,0,flag,x,y),
    5:lambda flag,x,y:can_turn_chess(chesses,-1,-1,flag,x,y),
    6:lambda flag,x,y:can_turn_chess(chesses,-1,1,flag,x,y),
    7:lambda flag,x,y:can_turn_chess(chesses,1,-1,flag,x,y)
    }
switch={
    0:lambda chess,flag,x,y:turn_chess(chess,0,1,flag,x,y),
    1:lambda chess,flag,x,y:turn_chess(chess,1,1,flag,x,y),
    2:lambda chess,flag,x,y:turn_chess(chess,1,0,flag,x,y),
    3:lambda chess,flag,x,y:turn_chess(chess,0,-1,flag,x,y),
    4:lambda chess,flag,x,y:turn_chess(chess,-1,0,flag,x,y),
    5:lambda chess,flag,x,y:turn_chess(chess,-1,-1,flag,x,y),
    6:lambda chess,flag,x,y:turn_chess(chess,-1,1,flag,x,y),
    7:lambda chess,flag,x,y:turn_chess(chess,1,-1,flag,x,y)
    }

rules(1,-100,-100)



while True:
    #logic:
    if gameover is False and AI:
        flag=1 if player else -1
        poslist=make_putpos(chesses,flag)
        if len(poslist)>0:
            if count0==1:
                pos=poslist[0]
            else:
                std_depth=random.randint(4,6) if len(poslist)<8 else random.randint(1,3)
                t=time.clock()
                print('search start with std_depth='+str(std_depth))
                P_list(chesses)
                pos=calc_value(chesses,-MAX_VALUE,MAX_VALUE,flag,0,std_depth if count0>std_depth else count0,64-count0)
                dtime=time.clock()-t
                #print('time:'+str(dtime))
                if(dtime<0.8):
                    time.sleep(0.8-dtime)
            chesses[pos[0]][pos[1]]=flag 
            player=not player
            AI=not AI
            rules(flag,pos[0],pos[1])
        else:
            player=not player
            AI= not AI
            needrefresh=True
    '''elif player==False:
         del chesses[:]
         chesses=[[0 for i in range(lengthofchessbox)] for j in range(lengthofchessbox)]
         chesses[int(lengthofchessbox/2)][int(lengthofchessbox/2)]=-1
         chesses[int(lengthofchessbox/2)-1][int(lengthofchessbox/2)-1]=-1
         chesses[int(lengthofchessbox/2)][int(lengthofchessbox/2)-1]=1
         chesses[int(lengthofchessbox/2)-1][int(lengthofchessbox/2)]=1
         player=not player
         rules(1 if player else -1,-100,-100)
         needrefresh=True
         gameover=False
         '''



    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type==MOUSEBUTTONUP:
            if gameover is False:
                mousex,mousey=pygame.mouse.get_pos()
                x,y=round((mousex-2*gapsize)/gapsize),round((mousey-2*gapsize)/gapsize)
                flag=1 if player else -1
                if(x>=0 and y>=0 and x<lengthofchessbox and y<lengthofchessbox and chesses[y][x]==0):     
                   vaildpos=False
                   for i in range(8):
                        if switch2[i](flag,y,x)[0]:
                            vaildpos=True
                            break
                   if vaildpos:
                        chesses[y][x]=flag 
                        player=not player
                        AI=not AI
                        rules(flag,y,x)
            else:
                 mousex,mousey=pygame.mouse.get_pos()
                 if mousex<10 and mousey<10:
                     del chesses[:]
                     rounds+=1
                     chesses=[[0 for i in range(lengthofchessbox)] for j in range(lengthofchessbox)]
                     chesses[int(lengthofchessbox/2)][int(lengthofchessbox/2)]=-1
                     chesses[int(lengthofchessbox/2)-1][int(lengthofchessbox/2)-1]=-1
                     chesses[int(lengthofchessbox/2)][int(lengthofchessbox/2)-1]=1
                     chesses[int(lengthofchessbox/2)-1][int(lengthofchessbox/2)]=1
                     rules(1 if player else -1,-100,-100)
                     AI=True if rounds%2 else False
                     player=True
                     canputchesspos=make_putpos(chesses,1)
                     needrefresh=True
                     gameover=False
            
            


    if needrefresh:
        #render:
        screen.fill(pygame.color.Color(135,206,250))
        #render chessbox:
        for i in range(lengthofchessbox+2):
            if i==0 or i==lengthofchessbox+1:
                pygame.draw.rect(screen,(0,0,0),pygame.rect.Rect((gapsize*(i+1),gapsize),(5 if i else -5,SCREEN_SIZE[1]-gapsize*2+5)))
            else:
                pygame.draw.aaline(screen,(0,0,0),(gapsize*(i+1),gapsize),(gapsize*(i+1),SCREEN_SIZE[1]-gapsize))
        for i in range(lengthofchessbox+2):
            if i==0 or i==lengthofchessbox+1:
                pygame.draw.rect(screen,(0,0,0),pygame.rect.Rect((gapsize,gapsize*(i+1)),(SCREEN_SIZE[0]-2*gapsize+5,5 if i else -5)))
            else:
                pygame.draw.aaline(screen,(0,0,0),(gapsize,gapsize*(i+1)),(SCREEN_SIZE[0]-gapsize,gapsize*(i+1)))
            pygame.draw.rect(screen,(0,0,0),pygame.rect.Rect((gapsize-6,gapsize-6),(6,6)))
        #render chess:
        for i in range(lengthofchessbox):
            for j in range(lengthofchessbox):
                if chesses[j][i]:
                    if chesses[j][i]==1:
                        pygame.draw.circle(screen,(0,0,0),((i+2)*gapsize,(j+2)*gapsize),int(chesssize))
                    else:
                        pygame.draw.circle(screen,(255,255,255),((i+2)*gapsize,(j+2)*gapsize),int(chesssize))
        
        for i in canputchesspos:
            pygame.draw.circle(screen,(0,0,255),((i[1]+2)*gapsize,(i[0]+2)*gapsize),int(chesssize*0.3))
        del canputchesspos[:]
        if gameover:
            pygame.draw.circle(screen,(255,0,0),(5,5),5)
            newfont=pygame.font.SysFont('system',25)
            surf=newfont.render('Black Wins' if count1>count2 else 'White Wins!' if count2>count1 else 'Draw',True,(0,0,0))
            screen.blit(surf,(SCREEN_SIZE[0]/2-surf.get_width()/2,0))
        else:
            if player:
                pygame.draw.circle(screen,(0,0,0),(5,5),5)
            else:
                pygame.draw.circle(screen,(255,255,255),(5,5),5)
            newfont=pygame.font.SysFont('system',25)
            surf=newfont.render('Computer Turn...'if AI else 'Player Turn...' ,True,(0,0,0))
            screen.blit(surf,(SCREEN_SIZE[0]/2-surf.get_width()/2,0))
        needrefresh=False
        screen.blit(font.render('Empty:'+str(count0),True,(0,0,0)),(10,0))
        screen.blit(font.render('Black:'+str(count1),True,(0,0,0)),(10,10))
        screen.blit(font.render('White:'+str(count2),True,(0,0,0)),(10,20))
        #final update:
        pygame.display.update()

       