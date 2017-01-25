from MinMax_AI import *
from MCT_AI import *

#the dict to map opposite
Opposite={'W':'B','B':'W'}

isHeld=lambda turn,pos:1 if pos==turn else 0
#the dict to map str dices to number 
Transform={'.':0,'W':1,'B':2}

class Othello_Game:    
    def __init__(self,data,can_withdraw=True):
        '''init of one game'''
        self.initdata=data
        self.__init_board(data)
        self.can_withdraw=can_withdraw
        if can_withdraw:
            self.init_withdraw_system()
        self.__vaild_check()

    def set_offensive(self, offensive):
        self.initdata=self.initdata[:2]+(offensive,random.choice(["B","W"]),self.initdata[4])


    def restart(self):
        '''restart a game'''
        self.__init_board(self.initdata)
        if self.can_withdraw:
            self.init_withdraw_system()
        self.__vaild_check()

    def __init_board(self,data):
        '''
        init a nested list with the data of row and col
        and put 4 dices on the board
        '''
        NUM_OF_ROWS,NUM_OF_COLS,FIRST_MOVE,TOP_LEFT,WIN_DETERMINE=data
        CHESS=[['.' for i in range(NUM_OF_ROWS)]for j in range(NUM_OF_COLS)]
        BOTTOM_RIGHT_Y=int(NUM_OF_COLS/2)
        BOTTOM_RIGHT_X=int(NUM_OF_ROWS/2)
        CHESS[BOTTOM_RIGHT_Y-1][BOTTOM_RIGHT_X-1]=TOP_LEFT
        CHESS[BOTTOM_RIGHT_Y][BOTTOM_RIGHT_X]=TOP_LEFT
        CHESS[BOTTOM_RIGHT_Y][BOTTOM_RIGHT_X-1]=Opposite[TOP_LEFT]
        CHESS[BOTTOM_RIGHT_Y-1][BOTTOM_RIGHT_X]=Opposite[TOP_LEFT]
        self.board=CHESS
        self.turn=FIRST_MOVE
        self.vaildpos=[]
        self.isover=False
        self.stats={'W':2,'B':2,'.':NUM_OF_COLS*NUM_OF_ROWS-4}
        self.width=NUM_OF_ROWS
        self.height=NUM_OF_COLS
        self.win_determine=WIN_DETERMINE
        self.probpoints=set([(BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X-2),(BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X-1),(BOTTOM_RIGHT_Y-1,BOTTOM_RIGHT_X-2),\
                         (BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X),(BOTTOM_RIGHT_Y-2,BOTTOM_RIGHT_X+1),(BOTTOM_RIGHT_Y-1,BOTTOM_RIGHT_X+1),\
                         (BOTTOM_RIGHT_Y,BOTTOM_RIGHT_X+1),(BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X+1),(BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X),\
                         (BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X-1),(BOTTOM_RIGHT_Y+1,BOTTOM_RIGHT_X-2),(BOTTOM_RIGHT_Y,BOTTOM_RIGHT_X-2),\
                         ])
   
    def init_withdraw_system(self):
        '''init some queue for user's withdraw'''
        self.pre_board=[]
        self.pre_probpoints=[]
        self.pre_turn=[]
        self.pre_vaildpos=[]
        self.pre_stats=[]
        self.pre_drop=[]
        self.pre_count=0


    def on_board(self,pos):
        '''determine if a position is on the game board'''
        y,x=pos
        return x>=0 and x<self.width and y<self.height and y>=0

    def cancel_drop(self):
        '''pop the queues to recover the board'''
        self.pre_count-=1
        self.board=self.pre_board.pop()
        self.probpoints=self.pre_probpoints.pop()
        self.turn=self.pre_turn.pop()
        self.vaildpos=self.pre_vaildpos.pop()
        self.stats=self.pre_stats.pop()
        self.isover=False
        pos=self.pre_drop.pop()
        return pos[0],pos[1],self.turn
        
    def __vaild_check(self):
        '''refresh the valid drop positions for current player(white or black)'''
        list=[]
        for i,j in self.probpoints:
            if self.board[i][j]=='.' and self.__vaild_drop((i,j)):
                list.append((i,j))
        self.vaildpos=list

    def __vaild_drop(self,pos):
        '''check if the position is vaild for current player'''
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    x=pos[1]+j
                    y=pos[0]+i
                    flag=False
                    while self.on_board((y,x)):
                        TEMP=self.board[y][x]
                        if TEMP=='.':
                            break
                        elif TEMP==Opposite[self.turn]:
                            flag=True
                        else:
                            if flag:
                                return True
                            else:
                                break
                        x+=j
                        y+=i
        return False


    def __Save_Game(self,pos=None):
        '''save current board and stats of the game'''
        self.pre_count+=1
        self.pre_board.append(copy.deepcopy(self.board))
        self.pre_probpoints.append(copy.deepcopy(self.probpoints))
        self.pre_turn.append(self.turn)
        self.pre_vaildpos.append(copy.deepcopy(self.vaildpos))
        self.pre_stats.append(copy.deepcopy(self.stats))
        self.pre_drop.append(pos)
    

    def __turn_the_dices(self,pos,i,j):
        '''turn the dices from one drop position to a single direction'''
        x=pos[1]+j
        y=pos[0]+i
        while self.on_board((y,x)):
            TEMP=self.board[y][x]
            if TEMP=='.':
                self.probpoints.add((y,x))
                break
            elif TEMP==self.turn:
                while x!=pos[1] or y!=pos[0]:
                    if self.board[y][x]!=self.turn:
                        self.board[y][x]=self.turn
                        self.stats[self.turn]+=1
                        self.stats[Opposite[self.turn]]-=1
                    x-=j
                    y-=i
                break
            x+=j
            y+=i

    
    def drop(self,pos):
        '''drop one dice on the game board and turn the dices(8 directions)'''
        assert(pos in self.vaildpos)
        if self.can_withdraw:
            self.__Save_Game(pos)
        self.probpoints.remove(pos)
        self.board[pos[0]][pos[1]]=self.turn
        self.stats[self.turn]+=1
        self.stats['.']-=1
        for i in range(-1,2):
            for j in range(-1,2):
                if i!=0 or j!=0:
                    self.__turn_the_dices(pos,i,j)
        self.turn=Opposite[self.turn]
        self.__vaild_check()
        if self.vaildpos==[]:
            self.turn=Opposite[self.turn]
            self.__vaild_check()
            if self.vaildpos==[]:
                self.isover=True

            

    def get_stats(self):
        '''simply return self.stats'''
        return self.stats

    def get_winner(self):
        '''determine who is the winner and return a str to represent it'''
        d=self.get_stats()
        if self.win_determine=='>':
            return 'W' if d['W']>d['B'] else 'B' if d['B']>d['W'] else 'NONE'
        else:
            return 'W' if d['W']<d['B'] else 'B' if d['B']<d['W'] else 'NONE'




if __name__=="__main__":
    count_MM_win=0
    count_MCT_win=0
    count_Random_win=0
    count=0
    MMAI=MinMax_AI((8,8))
    while True:
        print("game {} start...".format(count+1))
        first=random.choice(["W","B"])
        initdata=(8,8,first,random.choice(["W","B"]),'>')
        game=Othello_Game(initdata,False)
        MCTAI=MCT_Node.load()
        root=MCTAI
        count_drop=0
        i=random.choice([0,1])
        if i==0:
            MMAI_turn=first
        else:
            MMAI_turn=Opposite[first]
        while not game.isover:
            if game.turn==MMAI_turn:
                temp=MMAI.AI_move_input(game)
                MCTAI=MCTAI.get_next(temp)
                print("MM :{} player drop {}".format(game.turn,temp))
                game.drop(temp)
            else:
                temp=MCTAI.MCTS(game)
                MCTAI=MCTAI.get_next(temp)
                print("MCT:{} player drop {}".format(game.turn,temp))
                game.drop(temp)
            count_drop+=1
        if MMAI_turn==game.get_winner():
            count_MM_win+=1
        else:
            count_MCT_win+=1
        count+=1
        print('\nMCT: win:{} count:{} win_rate:{}'.format(count_MCT_win,count,count_MCT_win/count))
        print('MM: win:{} count:{} win_rate:{}'.format(count_MM_win,count,count_MM_win/count))
        root.save()
