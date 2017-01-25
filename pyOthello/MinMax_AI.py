from Othello_Game import *
import copy



#the max value of AI estimate
MAX_VALUE=100000000
'''
the struct for store information in a hash table
key for hashkey
depth for the depth of the situation of the game
lower for min value of this situation
upper for max value of this situation
move for the position to drop
'''
class hash_unit:
    def __init__(self):
        self.key=0
        self.depth=-1
        self.lower=0
        self.upper=0
        self.move=None


class MinMax_AI:
    def __init__(self,data):
        self.__init_AI(data)
        self.__init_hash_table(data)
        self.__init_value_matrix(data)
        
    def __generate_hash_key(self,game):
        '''according to current situation to create a hashkey'''
        self.hashkey=0
        for i in range(game.height):
            for j in range(game.width):
                self.hashkey^=self.zobrist[Transform[game.board[i][j]]][i][j]


    def __init_AI(self,data):
        '''init some attributes for AI'''
        NUM_OF_ROWS,NUM_OF_COLS=data
        self.AI_timer=0
        self.AI_max_time=5
        self.AI_base_depth=1
        self.AI_simple_eval=True if NUM_OF_ROWS*NUM_OF_COLS==16 else False
        self.AI_timer_start=0
        
    def __init_hash_table(self,data):
        '''init hash table for AI'''
        NUM_OF_ROWS,NUM_OF_COLS=data
        self.zobrist=None
        self.hash_table=None
        self.table_size=0
        self.__generate_zobrist(NUM_OF_ROWS,NUM_OF_COLS)
        self.pre_hashkey=[]

    def __init_value_matrix(self,data):
        '''init the estimated value for AI to evaluate the score of a situation'''
        NUM_OF_ROWS,NUM_OF_COLS=data
        self.values=[[(i-NUM_OF_ROWS/2)**2+(j-NUM_OF_COLS/2)**2 for i in range(NUM_OF_ROWS)]for j in range(NUM_OF_COLS)]
        for i in range(-2,2,3):
            for j in range(-2,2,3):
                self.values[i][j]*=-1
        for i in range(-1,1):
            for j in range(-1,1):
                self.values[i][j]*=4
        self.values[0][1]*=-1
        self.values[1][0]*=-1
        self.values[0][-2]*=-1
        self.values[1][-1]*=-1
        self.values[-1][-2]*=-1
        self.values[-2][-1]*=-1
        self.values[-1][1]*=-1
        self.values[-2][0]*=-1

    def __generate_zobrist(self,NUM_OF_ROWS,NUM_OF_COLS):
        '''generate a huge hash table and fill it with empty hash_unit'''
        self.zobrist=[[[random.getrandbits(15)^(random.getrandbits(15)<<15)^(random.getrandbits(15)<<30)^(random.getrandbits(15)<<45)^(random.getrandbits(15)<<60) for i in range(NUM_OF_ROWS)]for j in range(NUM_OF_COLS)]for k in range(3)]
        self.table_size=2**17
        self.hash_table=[hash_unit() for i in range(self.table_size)]

    def __evaluate(self,flag,game):
        '''
        AI evaluate the score of current situation
        based on:
        the difference of its dices and opponent's dices
        estimated score on value martix
        how many corners are occupied by itself
        the probability of occupying a corner in the next drop
        how many vaild position it and the opponent have
        how many dices are on the four sides
        '''
        if game.isover:
            winner=game.get_winner()
            if winner=='W':
                return -MAX_VALUE
            elif winner=='B':
                return MAX_VALUE
            else:
                return 0
        result=10*self.__dices_difference(flag,game)\
                    +800*self.__corner_occupied(flag,game)\
                    +400*self.__corner_adjacent(flag,game)\
                    +75*self.__dices_side(flag,game)\
                    +10*self.__martix_score(flag,game)
        return result if game.win_determine=='>' else -result

    
    def __dices_difference(self,flag,game):
        '''
        calculate the difference of AI's dices and opponent's dices
        and return as percentage
        '''
        opp=Opposite[flag]
        num_flag=0
        num_opp=0
        for i in range(game.height):
            for j in range(game.width):
                if game.board[i][j]==flag:
                    num_flag+=1
                elif game.board[i][j]==opp:
                    num_opp+=1
        if num_opp>num_flag:
            return 100*num_flag/(num_opp+num_flag)
        elif num_opp<num_flag:
            return -100*num_opp/(num_opp+num_flag)
        else:
            return 0


    def __corner_occupied(self,flag,game):
        '''
        calculate how many corners are occupied by AI and the opponent
        and return a weighted score
        '''
        num=0
        opp=Opposite[flag]
        ps=(game.board[0][0],game.board[0][-1],game.board[-1][0],game.board[-1][-1])
        for p in ps:
            if p==flag:
                num+=1
            elif p==opp:
                num-=1
        return 25*num
        
    def __corner_adjacent(self,flag,game):
        '''
        calculate the probability of occupying a corner in the next drop
        and return a weighted score
        '''
        return 12.5*(self.__helper_corner_adjacent(Opposite[flag],game)-self.__helper_corner_adjacent(flag,game))
                             
    def __helper_corner_adjacent(self,flag,game):
        '''
        calculate how many positions adjacent to the corner are occupied by a player
        and return the number
        '''
        num=0
        if game.board[0][0]=='.':
            num+=1 if game.board[1][0]==flag else 0
            num+=1 if game.board[0][1]==flag else 0
            num+=1 if game.board[1][1]==flag else 0
        if game.board[0][-1]=='.':
            num+=1 if game.board[0][-2]==flag else 0
            num+=1 if game.board[1][-1]==flag else 0
            num+=1 if game.board[1][-2]==flag else 0
        if game.board[-1][-1]=='.':
            num+=1 if game.board[-1][-2]==flag else 0
            num+=1 if game.board[-2][-1]==flag else 0
            num+=1 if game.board[-2][-2]==flag else 0
        if game.board[-1][0]=='.':
            num+=1 if game.board[-1][1]==flag else 0
            num+=1 if game.board[-2][0]==flag else 0
            num+=1 if game.board[-2][1]==flag else 0
        return num

    def __dices_side(self,flag,game):
        '''
        calculate how many AI's dices on the four sides 
        and return the number
        '''
        num=0
        for i in range(game.height):
            for j in range(game.width):
                if not self.__isCorner(i,j,game):
                    break;
                if game.board[i][j]==flag:
                    if i==0 or i==col:
                        if game.board[i][j-1]=='.' and game.board[i][j+1]=='.':
                            num+=1
                    elif j==0 or j==row:
                        if game.board[i-1][j]=='.' and game.board[i+1][j]=='.':
                            num+=1
                    else:
                        if game.board[i-1][j]=='.' and game.board[i-1][j-1]=='.'\
                           and game.board[i][j-1]=='.' and game.board[i+1][j-1]=='.'\
                           and game.board[i+1][j]=='.' and game.board[i+1][j+1]=='.'\
                           and game.board[i][j+1]=='.' and game.board[i-1][j+1]=='.':
                            num+=1
        return num
                
    def __martix_score(self,flag,game):
        '''
        according to the estimated score matrix
        simply summing up all AI dices
        minus the sum of all opponent dices
        '''
        opp=Opposite[flag]
        num=0
        for i in range(game.height):
            for j in range(game.width):
                temp=game.board[i][j]
                if temp==flag:
                    num+=self.values[i][j]
                elif temp==opp:
                    num-=self.values[i][j]
        return num



    def __isCorner(self,i,j,game):
        '''
        determine if the i j in the game board is a corner
        '''
        if i==0:
            if j==0 or j==len(game.board[0]):
                return True
        elif i==len(game.board):
            if j==0 or j==len(game.board[0]):
                return True
        return False

    def AI_move_input(self,game):
        '''
        let the AI think deeper and deeper until time is up
        and return the best move at that time
        '''
        game=copy.deepcopy(game)
        game.can_withdraw=True
        game.init_withdraw_system()
        depth=self.AI_base_depth
        self.__generate_hash_key(game)
        result=0
        pre=None
        while True:
            try:
                result=self.__calc_value(-MAX_VALUE,MAX_VALUE,0,depth,game)[1]
                if result!=None:
                    pre=result
                depth+=2
                if depth>game.stats['.']-1:
                    break
            except Exception as e:
                #print(e)
                break
        self.AI_timer=0
        self.AI_timer_start=0
        return pre 




    def __calc_value(self,a,b,depth,max_depth,game):
        '''
        the most important part of AI
        based on Principal Variation Search(PVS) and Alpha-beta Pruning
        blending with zobrist hash table
        '''
        #if the time is up
        #break out
        if self.AI_timer>self.AI_max_time:
            for i in range(depth):
                game.cancel_drop()
            raise 
        #init max_value
        max_value=-MAX_VALUE
        #see if the situation is in the hash table
        #if true, pruning 
        if depth!=0:
            hashunit=self.__CheckHash(depth)
            if hashunit!=None:
                if hashunit.lower>a:
                    a=hashunit.lower
                    if a>=b:
                        self.__Update_Timer()
                        return a,None
                if hashunit.upper<b:
                    b=hashunit.upper
                    if b<=a:
                        self.__Update_Timer()
                        return b,None
        #see if the game is over or the depth reaches the limit
        #if true, directly return the score of current situation
        if game.isover or depth==max_depth:
            val=self.__evaluate(game.turn,game)
            self.__Update_Timer()
            return val,None
        #init the best move
        move=(game.vaildpos[0][0],game.vaildpos[0][1])
        #try to drop every vaild move
        for i in game.vaildpos:
            self.pre_hashkey.append(self.hashkey)
            game.drop(i)
            #if no vaild drop is found, continue searching
            if max_value==-MAX_VALUE:
                value=-self.__calc_value(-b,-max(a,max_value),depth+1,max_depth,game)[0]
            else:
                #try Minimal Window Search
                value=-self.__calc_value(-a-1,-a,depth+1,max_depth,game)[0]
                if value>a:
                    a=value
                    #if there is no pruning 
                    if a<b:
                        #continue searching
                        value=-self.__calc_value(-b,-max(a,max_value),depth+1,max_depth,game)[0]
            game.cancel_drop()
            self.hashkey=self.pre_hashkey.pop()
            self.__SaveHash(depth,value,i,a,b)
            #update max_value and the best move
            if value>max_value:
                max_value=value
                move=i
            #if this drop is the best
            if max_value>a:
                #update the floor of score
                a=max_value
            #if this drop is not good 
            if max_value>=b:
                #pruning
                self.__Update_Timer()
                return max_value,move
        self.__Update_Timer()
        return max_value,move         

    def __SaveHash(self,depth,value,i,a,b):
        '''
        function to save current data to hash table
        '''
        if value>=b:
            self.__RecordHash(depth,value,MAX_VALUE,i)
        elif value<=a:
            self.__RecordHash(depth,-MAX_VALUE,value,i)
        else:
            self.__RecordHash(depth,value,value,i)
                
    def __Update_Timer(self):
        '''
        update the AI's timer to ensure its time of thinking is constant
        '''
        if self.AI_timer_start==0:
            self.AI_timer_start=time.time()
        else:
            self.AI_timer+=time.time()-self.AI_timer_start
            self.AI_timer_start=time.time()


    def __CheckHash(self,depth):
        '''
        see if there is a same situation in the hash table
        it must deeper than current depth
        '''
        index=self.hashkey%self.table_size
        unit=self.hash_table[index]
        if unit.depth==-1 or unit.key!=self.hashkey or unit.depth<=depth:
            return None
        return unit

    def __RecordHash(self,depth,lower,upper,extra):
        '''record deeper situation to the hash table'''
        index=self.hashkey%self.table_size
        if self.hash_table[index].depth>=depth:
           return
        self.hash_table[index].key=self.hashkey
        self.hash_table[index].depth=depth
        self.hash_table[index].upper=upper
        self.hash_table[index].lower=lower
        self.hash_table[index].move=extra






    
