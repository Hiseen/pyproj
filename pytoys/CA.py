#CA


WIDTH=int(input('Please enter the width of the CA: '))
HEIGHT=int(input('Please enter the height of the CA: '))



import tkinter
import time
import random
import copy
from time import clock
def SAFE_get(livespace,y,x):
    global WIDTH,HEIGHT
    if y>=0 and y<HEIGHT and x>=0 and x<WIDTH:
        return livespace[y][x]
    else:
        return 0
        


def cellrule(livespace,y,x):
    cells_around=\
    SAFE_get(livespace,y+1,x)+\
    SAFE_get(livespace,y-1,x)+\
    SAFE_get(livespace,y,x+1)+\
    SAFE_get(livespace,y,x-1)+\
    SAFE_get(livespace,y+1,x+1)+\
    SAFE_get(livespace,y-1,x+1)+\
    SAFE_get(livespace,y+1,x-1)+\
    SAFE_get(livespace,y-1,x-1)
    if livespace[y][x]==1:
        if cells_around<2:
            return 0
        elif cells_around>3:
            return 0
        else:
            return 1
    else:
        if cells_around==1:
            return 1
        else:
            return 0
    

def drawstaff(cellrule,livespace,canvas):
    global WIDTH,HEIGHT
    while True:
        #start=clock()
        #copy1=copy.deepcopy(livespace)
        copy1=[livespace[i][:] for i in range(HEIGHT)]
        #mid=clock()
        #print(mid-start)
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cellrule(livespace,i,j):
                    copy1[i][j]=1
                    canvas.create_rectangle(j,i,j,i)
                else:
                    copy1[i][j]=0
        livespace=copy1
        #finish=clock()
        #print(finish-mid)
        canvas.update()
        time.sleep(0.01)
        canvas.delete(tkinter.ALL)
                    
                    






def display(cellrule):
    global WIDTH,HEIGHT
    livespace=[[0 for i in range(WIDTH)]for j in range(HEIGHT)]
    '''for i in range(int(HEIGHT)):
        for j in range(int(WIDTH)):
            result=random.randrange(0,30)
            if result==0:
                livespace[i][j]=1'''
                
    livespace[int(HEIGHT/2)+1][int(WIDTH/2)+1]=1
    livespace[int(HEIGHT/2)+1][int(WIDTH/2)-1]=1
    livespace[int(HEIGHT/2)-1][int(WIDTH/2)+1]=1
    livespace[int(HEIGHT/2)-1][int(WIDTH/2)-1]=1
    livespace[int(HEIGHT/2)][int(WIDTH/2)]=1
    my_window = tkinter.Tk()
    my_window.title('Cellular Automata')
    my_canvas = tkinter.Canvas(my_window, width=WIDTH, height=HEIGHT)  
    my_canvas.pack()
    drawstaff(cellrule,livespace,my_canvas)
    my_window.mainloop()


display(cellrule)

    
