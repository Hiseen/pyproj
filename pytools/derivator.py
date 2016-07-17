import re
import math


_precedence={'(':0,')':0,
             '-':1,'+':1,
             '*':2,'/':2,
             'plus':3,'minus':3,'sin':3,'cos':3,'tan':3,'log':3,
             '^':4
             }

_operators='-+*/^'

_functions=['sin','cos','tan','log']

_symboldict_reserved='symbol'

class derivator(object):
    def __init__(self,*args,**kwargs):
        assert all(not _symboldict_reserved in i for i in args),"any word contains '{}' cannot be a vaild variable name".format(_symboldict_reserved)
        assert all(not _symboldict_reserved in i for i in kwargs),"any word contains '{}' cannot be a vaild variable name".format(_symboldict_reserved)
        self.vars=[i for i in args]
        self.exps={i:kwargs[i] for i in kwargs}
        
    def get_derivative(self,str_exp):
        IsMulVars=[re.search(i,str_exp) for i in self.vars].count(None)!=len(self.vars)-1
        if IsMulVars:
            #for every var, output a derivative
            pass
        else:
            return self.recursive_helper(*self.split_exp(str_exp))
            
            
    def recursive_helper(self,sd,key):
        if not key:
            return ''
        if not key in sd:
            if key in self.vars:
                return '1';
            else:
                return '0';
        op=sd[key][1]
        if (op=='+' or op=='-') and not sd[key][0]:
            return op+self.recursive_helper(sd,sd[key][2])
        elif op=='*':
            return self.recursive_helper(sd,sd[key][0])+'*'+self.recursive_get_exp(sd,sd[key][2])+'+'+\
                   self.recursive_helper(sd,sd[key][2])+'*'+self.recursive_get_exp(sd,sd[key][0])
        elif op=='/':
            return '('+self.recursive_helper(sd,sd[key][0])+'*'+self.recursive_get_exp(sd,sd[key][2])+'-'+\
                   self.recursive_helper(sd,sd[key][2])+'*'+self.recursive_get_exp(sd,sd[key][0])+')/'+self.recursive_get_exp(sd,sd[key][2])+'**2'
        elif (op=='+'or op=='-'):
            return self.recursive_helper(sd,sd[key][0])+op+self.recursive_helper(sd,sd[key][2])
        elif op=='^':
            f="math.e**({}*math.log({}))".format(self.recursive_get_exp(sd,sd[key][2]),self.recursive_get_exp(sd,sd[key][0]))
            sd=self.symboldict_add(sd,(None,'log',sd[key][0]))
            key1=_symboldict_reserved+str(len(sd))
            sd=self.symboldict_add(sd,(sd[key][2],'*',key1))
            return f+'*('+self.recursive_helper(sd,_symboldict_reserved+str(len(sd)))+')'
        elif op=='sin':
            return 'math.cos('+self.recursive_get_exp(sd,sd[key][2])+')*('+self.recursive_helper(sd,sd[key][2])+')'
        elif op=='cos':
            return '-math.sin('+self.recursive_get_exp(sd,sd[key][2])+')*('+self.recursive_helper(sd,sd[key][2])+')'
        elif op=='tan':
            return self.recursive_helper(sd,sd[key][2])+'*math.sec({})**2'.format(self.recursive_get_exp(sd,sd[key][2]))
        elif op=='log':
            return self.recursive_helper(sd,sd[key][2])+'*(1/{})'.format(self.recursive_get_exp(sd,sd[key][2]))
        else:
            raise NotImplementedError

    def symboldict_add(self,sd,value):
        key=_symboldict_reserved+str(len(sd)+1)
        sd[key]=value
        return sd


    def recursive_get_exp(self,sd,key):
        if not key:
            return ''
        elif key in self.vars:
            return key
        try:
            if isinstance(eval(key),float) or isinstance(eval(key),int):
                return key
        except:
            result=''
            endflag=False
            if sd[key][0] in sd:
                result+='('+self.recursive_get_exp(sd,sd[key][0])+')'
            else:
                result+=sd[key][0] if sd[key][0] else ''
            if sd[key][1] in _operators:
                if sd[key][1]=='^':
                    result+='**'
                else:
                    result+=sd[key][1]
            elif sd[key][1] in _functions:
                result+='math.'+sd[key][1]+'('
                endflag=True
            if sd[key][2] in sd:
                result+='('+self.recursive_get_exp(sd,sd[key][2])+')'
            else:
                result+=sd[key][2]
            if endflag:
                result+=')'
            return result






           
    def split_exp(self,str_exp):
        tempRPN=self.generate_RPN(str_exp)
        stack=[]
        symboldict={}
        last=''
        for i in tempRPN:
            if isinstance(i,tuple):
                stack.append(i[0])
            else:
                temp=stack.pop()
                if i=='minus':
                    data=(None,'-',temp)
                elif i=='plus':
                    data=(None,'+',temp)
                elif i in _operators:
                    data=(stack.pop(),i,temp)
                elif i in _functions:
                    data=(None,i,temp)
                key=_symboldict_reserved+str(len(symboldict)+1)
                symboldict[key]=data
                last=key
                stack.append(key)
        return symboldict,last    

    def generate_RPN(self,str_exp):
        stack=[]
        final_stack=[]
        i=0
        while i<len(str_exp):
            char=str_exp[i]
            if (char=='-' or char=='+') and ((i>1 and str_exp[i-1]=='(') or i==0):
                char='minus' if char=='-' else 'plus'
            else:
                for k in _functions:
                    if str_exp[i:i+len(k)]==k:
                        char=k
                        i+=len(k)-1
                        break
            if char.isdigit():
                end=i+1
                while end<len(str_exp) and (str_exp[end].isdigit() or str_exp[end]=='.'):
                    end+=1
                final_stack.append((str_exp[i:end],'num'))
                i=end
            else:
                flag=False
                for k in self.vars:
                    if str_exp[i:i+len(k)]==k:
                        final_stack.append((k,'var'))
                        flag=True
                        break
                if not flag:
                    for k in self.exps:
                        if str_exp[i:i+len(k)]==k:
                            final_stack.extend(self.generate_RPN(self.exps[k]))
                            flag=True
                            break
                if not flag:
                    if char=='(':
                        stack.append(char)
                    elif char==')':
                        while stack[-1]!='(':
                            final_stack.append(stack.pop())
                        stack.pop()
                    else:
                        while len(stack) and _precedence[stack[-1]]>=_precedence[char]:
                            final_stack.append(stack.pop())
                        stack.append(char)
                i+=1
        stack.reverse()
        final_stack.extend(stack)
        return final_stack
                            
                
a=derivator('x','z',y='1000*2000')
print(a.get_derivative('sin(2*(x^(x/100)))'))
