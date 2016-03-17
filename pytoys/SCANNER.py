from collections import namedtuple

def enum(*keys):
    return namedtuple('Enum', keys)(*range(len(keys)))


TOKENS=enum('ID',\
            'EQUAL','ADD',\
            'MINUS','MUTI',\
            'DIVIDE','LP',\
            'RP','LSB',\
            'RSB','LAB',\
            'RAB','LB',\
            'RB','INT',\
            'STR','FLOAT',\
            'EOF')

OPERATORS={'+':TOKENS.ADD,'-':TOKENS.MINUS,'*':TOKENS.MUTI,'\\':TOKENS.DIVIDE,\
           '[':TOKENS.LSB,']':TOKENS.RSB,'(':TOKENS.LP,')':TOKENS.RP,\
           '{':TOKENS.LB,'}':TOKENS.RB,'=':TOKENS.EQUAL,'<':TOKENS.LAB,'>':TOKENS.RAB}

SKIPS=(' ','\t','\n','\r')

class TOKEN_UNIT:
    def __init__(self,token,value):
        self.TOKEN=token
        self.VALUE=value
    def __str__(self):
        return '({},{})'.format(self.TOKEN,self.VALUE)



class SCANNER:
    def __init__(self,data):
        self.raw_data=data
        self.now_pos=0

    def eat_token(self):
        self.now_pos+=1

    def ID_token(self):
        result_value=''
        while self.now_pos<len(self.raw_data) and not self.raw_data[self.now_pos] in OPERATORS.keys() and not self.raw_data[self.now_pos] in SKIPS:
            result_value+=self.raw_data[self.now_pos]
            self.eat_token()
        return TOKEN_UNIT(TOKENS.ID,result_value)
    def INT_token(self):
        result_value=''
        while self.now_pos<len(self.raw_data) and self.raw_data[self.now_pos].isdigit():
            result_value+=self.raw_data[self.now_pos]
            self.eat_token()
        return TOKEN_UNIT(TOKENS.INT,result_value)
        
    def scan(self):
        if self.now_pos>=len(self.raw_data):
            return TOKEN_UNIT(TOKENS.EOF,None)
        while self.raw_data[self.now_pos] in SKIPS:
            self.eat_token()
            if self.now_pos>=len(self.raw_data):
                return TOKEN_UNIT(TOKENS.EOF,None) 
        temp=self.raw_data[self.now_pos]
        if temp in OPERATORS.keys():
            self.eat_token()
            return TOKEN_UNIT(OPERATORS[temp],temp)
        if temp.isalpha():
            return self.ID_token()
        if temp.isdigit():
            return self.INT_token()



data='''abc=0 b=1213123 c=abc+b
qwe=asdsa
sada=qweqwe
123213=324sad
'''
S1=SCANNER(data)
while True:
    temp=S1.scan()
    print(temp)
    if temp.TOKEN==TOKENS.EOF:
        break
        














            
