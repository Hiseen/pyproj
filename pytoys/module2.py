import pygame
import time
class binaryNode:
    def __init__(self,val=0, **kwargs):
        self.right=None
        self.left=None
        self.val=val
        self.depth=0
        return super().__init__(**kwargs)

import random
SCREEN_SIZE=(1200,600)


def PreSearch(N,result):
    if N.left:
        PreSearch(N.left,result)
    result.append(N.val)
    if N.right:
        Preseach(N.right,result)

def AvlidList(l):
    for i in l:
        if i:
            return True
    return False


def StackSearch(N,result):
    nl=[]
    if N.left:
        nl.append(N.left)
    else:
        nl.append(None)
    if N.right:
        nl.append(N.right)
    else:
        nl.append(None)
    result.append([N.val])
    result.append([i.val if i else None for i in nl])
    stop=not AvlidList(nl)
    while(stop is False):
        nnl=[]
        for i in nl:
            if i:
                if i.left:
                    nnl.append(i.left)
                else:
                    nnl.append(None)
                if i.right:
                    nnl.append(i.right)
                else:
                    nnl.append(None)
        nl=nnl[:]
        stop=not AvlidList(nl)
        if stop is False:
            result.append([i.val if i else None for i in nl])



def CreateNodes(l,curN,curIndex):
    if not curN or curIndex<0 or curIndex>=len(l):
        return 
    last=len(l)-1
    if 2*curIndex+1<=last:
        curN.left=binaryNode(l[2*curIndex+1])
    else:
        curN.left=None
    if 2*curIndex+2<=last:
        curN.right=binaryNode(l[2*curIndex+2])
    else:
        curN.right=None
    CreateNodes(l,curN.left,2*curIndex+1)
    CreateNodes(l,curN.right,2*curIndex+2)

'''
def CreateBSTNodes(node,val):
    if val>node.val:
        if node.right:
            CreateBSTNodes(node.right,val)
            if 2==Height(node.right)-Height(node.left):
                if val>node.right.val:
                    node=RotationRO(node)
                else:
                    node=RotationRT(node)
        else:
            node.right=binaryNode(val)
            return
    elif val<node.val:
        if node.left:
            CreateBSTNodes(node.left,val)
            if 2==Height(node.left)-Height(node.right):
                if val<node.left.val:
                    node=RotationLO(node)
                else:
                    node=RotationLT(node)
        else:
            node.left=binaryNode(val)
            return
    else:
       return

'''
def CreateBSTNodes(node,val):
    if node is None:
        node=binaryNode(val)
    elif val>node.val:
        node.right=CreateBSTNodes(node.right,val)
        if 2==Height(node.right)-Height(node.left):
            if val>node.right.val:
                node=RotationRO(node)
            else:
                node=RotationRT(node)
    elif val<node.val:
        node.left=CreateBSTNodes(node.left,val)
        if 2==Height(node.left)-Height(node.right):
            if val<node.left.val:
                node=RotationLO(node)
            else:
                node=RotationLT(node)
    node.depth=max(Height(node.right),Height(node.left))+1
    return node

def Height(node):
    if node==None:
        return -1
    else:
        return node.depth


def RotationLO(node):
    k1=node.left
    node.left=k1.right
    k1.right=node
    node.depth=max(Height(node.right),Height(node.left))+1
    k1.depth=max(Height(k1.left),node.depth)+1
    return k1
def RotationRO(node):
    k1=node.right
    node.right=k1.left
    k1.left=node
    node.depth=max(Height(node.right),Height(node.left))+1
    k1.depth=max(Height(k1.right),node.depth)+1
    return k1

def RotationRT(node):
    node.right=RotationLO(node.right)
    return RotationRO(node)

def RotationLT(node):
    node.left=RotationRO(node.left)
    return RotationLO(node)

def Pre_reverse(node):
    temp=node.right
    node.right=node.left
    node.left=temp
    if node.left:
        node.left=Pre_reverse(node.left)
    if node.right:
        node.right=Pre_reverse(node.right)
    return node


def FindMin(node):
    if node.left:
        return FindMin(node.left)
    else:
        return node



def FindMax(node):
    if node.right:
        return FindMax(node.right)
    else:
        return node


'''
def BSTDeleteNode(node,val):
    if node==None:
        return 
    elif val<node.val:
        node=BSTDeleteNode(node.left,val)
    elif val>node.val:
        node=BSTDeleteNode(node.right,val)
    elif node.left and node.right:
        temp=FindMin(node.right)
        node.val=temp.val
        node=BSTDeleteNode(node.right,node.val)
    else:
        if node.left and not node.right:
            temp=FindMax(node.left)
            node.val=temp.val
            node=BSTDeleteNode(node.left,node.val)
        elif node.right and not node.left:
            temp=FindMin(node.right)
            node.val=temp.val
            node=BSTDeleteNode(node.right,node.val)
        else:
            del node
            node=None
            return
    if node:
         if 2==Height(node.left)-Height(node.right):
            if val<node.left.val:
                node=RotationLO(node)
            else:
                node=RotationLT(node)
         if 2==Height(node.right)-Height(node.left):
            if val>node.right.val:
                node=RotationRO(node)
            else:
                node=RotationRT(node)

'''
def BSTDeleteNode(node,val):
    if node is None:
        print('there is no such val:',val,' in the tree')
        return 
    elif val<node.val:
        node.left=BSTDeleteNode(node.left,val)
        if (Height(node.right)-Height(node.left))==2:
            if Height(node.right.right)>=Height(node.right.left):
                node=RotationRO(node)
            else:
                node=RotationRT(node)
        node.depth=max(Height(node.left),Height(node.right))+1
    elif val>node.val:
        node.right=BSTDeleteNode(node.right,val)
        if (Height(node.left)-Height(node.right))==2:
            if Height(node.left.left)>=Height(node.left.right):
                node=RotationLO(node)
            else:
                node=RotationLT(node)
        node.depth=max(Height(node.left),Height(node.right))+1
     
    elif node.left and node.right:
        if node.left.depth<=node.right.depth:
            minNode=FindMin(node.right)
            node.val=minNode.val
            node.right=BSTDeleteNode(node.right,node.val)
        else:
            maxNode=FindMax(node.left)
            node.val=maxNode.val
            node.left=BSTDeleteNode(node.left,node.val)
        node.depth=max(Height(node.left),Height(node.right))+1
    else:
        if node.right:
            node=node.right
        else:
            node=node.left
     
    return node


def NewBSTTree(N,l):
    N.val=l[0]
    for i in range(1,len(l)):
        N=CreateBSTNodes(N,l[i])
        yield (True,N)
    for i in range(47):
        N=BSTDeleteNode(N,i)
        yield (True,N)
    while True:
        i=int(input('key value'))
        N=BSTDeleteNode(N,i)
        yield (True,N)
    #N=Pre_reverse(N)
    yield (True,N)
    yield (False, N)


def NewBinaryTree(N,l):
    N.val=l[0]
    CreateNodes(l,N,0)
        
        

list1=[i for i in range(100)]
ROOT=binaryNode()


from pygame.locals import *
from sys import exit
pygame.init()
screen=pygame.display.set_mode(SCREEN_SIZE,0,32)
pygame.display.set_caption("wow")
time1=pygame.time.Clock()
needrefresh=False
font=pygame.font.SysFont('system',16)


#1 2 4 8 16

def drawNode(n,level,x):
    screen.blit(font.render(str(n.val),True,(255,255,255)),(int(x),int((level+1)*50)))
    #pygame.draw.circle(screen,(255,255,255),(int(x),int((level+1)*50)),n.val)
    if n.left is not None:
        pygame.draw.line(screen,(255,255,255),(int(x),int((level+1)*50)),(int(x-SCREEN_SIZE[0]/(2**(level+2))),int((level+2)*50)))
        drawNode(n.left,level+1,x-SCREEN_SIZE[0]/(2**(level+2)))
    if n.right is not None:
        pygame.draw.line(screen,(255,255,255),(int(x),int((level+1)*50)),(int(x+SCREEN_SIZE[0]/(2**(level+2))),int((level+2)*50))) 
        drawNode(n.right,level+1,x+SCREEN_SIZE[0]/(2**(level+2)))

fun=NewBSTTree(ROOT,list1)
needstop=True


while True:
    for event in pygame.event.get():
      if event.type == QUIT:
          exit()
    if needstop:
        needstop,ROOT=fun.__next__()
    #if needrefresh is False: 
    screen.fill(pygame.color.Color(0,0,0))
    drawNode(ROOT,0,SCREEN_SIZE[0]/2)
    pygame.display.update()
    #time.sleep(1)
        #needrefresh=True