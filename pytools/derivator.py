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
        self.symboldict={}
    def get_derivative(self,str_exp):
        self.symboldict={}
        IsMulVars=[re.search(i,str_exp) for i in self.vars].count(None)!=len(self.vars)-1
        if IsMulVars:
            #for every var, output a derivative
            pass
        else:
            return self.recursive_helper(self.split_exp(str_exp))
            
    def recursive_helper(self,key):
        if not key:
            return ''
        if not key in self.symboldict:
            if key in self.vars:
                return '1';
            else:
                return '0';
        left,op,right=self.symboldict[key]
        if (op=='+' or op=='-'):
            return self.combiner(self.recursive_helper(left),op,self.recursive_helper(right))
        elif op=='*':
            return self.combiner(self.combiner(self.recursive_helper(left),'*',self.recursive_get_exp(right)),'+',\
                   self.combiner(self.recursive_helper(right),'*',self.recursive_get_exp(left)))
        elif op=='/':
            return self.combiner(self.combiner(self.combiner(self.recursive_helper(left),'*',self.recursive_get_exp(right)),'-',\
                   self.combiner(self.recursive_helper(right),'*',self.recursive_get_exp(left))),'/',self.combiner(self.recursive_get_exp(right),'^','2'))
        elif op=='^':
            n=self.is_num(right)
            if n:
                return self.combiner(str(n),'*',self.combiner(left,'^',str(n-1)))
            else:
                f=self.combiner(self.recursive_get_exp(left),'^',self.recursive_get_exp(right))
                key=self.symboldict_add((None,'log',left))
                key=self.symboldict_add((right,'*',key))
                return self.combiner(f,'*',self.recursive_helper(key))
        elif op=='sin':
            return self.combiner(self.combiner(None,'cos',self.recursive_get_exp(right)),'*',self.recursive_helper(right))
        elif op=='cos':
            return self.combiner(None,'-',self.combiner(self.combiner(None,'sin',self.recursive_get_exp(right)),'*',self.recursive_helper(right)))
        elif op=='tan':
            return self.combiner(self.recursive_helper(right),'*','math.sec({})**2'.format(self.recursive_get_exp(right)))
        elif op=='log':
            return self.combiner(self.recursive_helper(right),'*',self.combiner('1','/',self.recursive_get_exp(right)))
        else:
            raise NotImplementedError

    def is_num(self,str):
        try:
            num=eval(str)
            if isinstance(num,int) or isinstance(num,float):
                return num
            else:
                return False
        except:
            return False


    def combiner(self,left,op,right):
        if right:
            for i in right:
                if i in _operators:
                    if _precedence[i]<_precedence[op]:
                        right='('+right+')'
                        break
        if left:
            for i in left:
                if i in _operators:
                    if _precedence[i]<_precedence[op]:
                        left='('+left+')'
                        break
        if op=='*':
            if left=='0' or right=='0' or left=='' or right=='':
                return ''
            elif left=='1':
                return right
            elif right=='1':
                return left
        elif op=='/':
            assert right!='0' and right!=''
            if left=='0' or left=='':
                return ''
        elif op=='+':
            if not left or left=='0' or left=='':
                return right
            elif right=='0' or right=='':
                return left
        elif op=='-':
            if not left or left=='0' or left=='':
                return op+right
            elif right=='0' or right=='':
                return left
        elif op=='^':
            assert (left!='0' and left!='') or (right!='0' and right!='')
            if left=='0':
                return '0'
            elif right=='0':
                return '1'
            elif left=='1':
                return '1'
            elif right=='1':
                return left
            else:
                return left+'**'+right
        elif op in _functions:
            return 'math.{}({})'.format(op,right if not right.startswith('(') else right[1:-1])
        else:
            raise NotImplementedError
        
        return left+op+right


    def symboldict_add(self,value):
        key=_symboldict_reserved+str(len(self.symboldict)+1)
        self.symboldict[key]=value
        return key


    def recursive_get_exp(self,key):
        if not key:
            return ''
        elif key in self.vars:
            return key
        elif self.is_num(key):
            return key
        else:
            result=''
            left,op,right=self.symboldict[key]
            if left in self.symboldict:
                left=self.recursive_get_exp(left)
            if right in self.symboldict:
                right=self.recursive_get_exp(right)
            return self.combiner(left,op,right)
           
    def split_exp(self,str_exp):
        tempRPN=self.generate_RPN(str_exp)
        stack=[]
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
                last=self.symboldict_add(data)
                stack.append(last)
        return last    

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
t=a.get_derivative('sin(x^((2*x+50*x)/(100-x)))')
print(t)
f1=eval('lambda x:'+t)
f2=eval('lambda x:'+input())
for i in range(1,30):
    print(f1(i),f2(i))






