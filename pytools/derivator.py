import re
import math


_precedence={'(':0,')':0,
             '-':1,'+':1,
             '*':2,'/':2,
             'plus':3,'minus':3,'sin':3,'cos':3,'tan':3,'log':3,
             '^':4
             }

_operators='-+*/^minusplus'

_functions=['sin','cos','tan','log']

_symboldict_reserved='symbol'

_DEBUG=False

_math_const=['e','pi']

_opt_table={
    ('0','+','var'):lambda x,y:(y.left,y.right,y.symbol),
    ('var','+','0'):lambda x,y:(x.left,x.right,x.symbol),
    ('0','*','var'):lambda x,y:(None,None,Symbol('0')),
    ('var','*','0'):lambda x,y:(None,None,Symbol('0')),
    ('1','*','var'):lambda x,y:(y.left,y.right,y.symbol),
    ('var','*','1'):lambda x,y:(x.left,x.right,x.symbol),
    ('1','^','var'):lambda x,y:(None,None,Symbol('1')),
    ('var','^','1'):lambda x,y:(x.left,x.right,x.symbol),
    ('var','^','0'):lambda x,y:(None,None,Symbol('1')),
    ('var','/','1'):lambda x,y:(x.left,x.right,x.symbol),
    ('0','*','op'):lambda x,y:(None,None,Symbol('0')),
    ('op','*','0'):lambda x,y:(None,None,Symbol('0')),
    ('0','+','op'):lambda x,y:(y.left,y.right,y.symbol),
    ('op','+','0'):lambda x,y:(x.left,x.right,x.symbol),
    ('1','*','op'):lambda x,y:(y.left,y.right,y.symbol),
    ('op','*','1'):lambda x,y:(x.left,x.right,x.symbol),
    ('var','*','num'):lambda x,y:(y,x,Symbol('*')),
    ('0','-','op'):lambda x,y:(None,y,Symbol('minus')),
    ('0','-','var'):lambda x,y:(None,y,Symbol('minus')),
    ('var','-','var'):lambda x,y:(None,None,Symbol('0')),
    ('var','+','var'):lambda x,y:(x,AST_Node(Symbol('2')),Symbol('*')),
    ('var','*','var'):lambda x,y:(x,AST_Node(Symbol('2')),Symbol('^')),
    ('var','/','var'):lambda x,y:(None,None,Symbol('1')),
    ('op','*','num'):lambda x,y:(y,x,Symbol('*')),
    }

_opt_rules2={
    ('op','+',('op','*','num')):lambda l,rl,rr:((AST_Node(Symbol(str(eval(rr.symbol.value)+1))),l,Symbol('*')) if l==rl else None),
    ('op','+',('num','*','op')):lambda l,rl,rr:((AST_Node(Symbol(str(eval(rl.symbol.value)+1))),l,Symbol('*')) if l==rr else None),
    ('op','-',('op','*','num')):lambda l,rl,rr:((AST_Node(Symbol(str(eval(rr.symbol.value)-1))),l,Symbol('*')) if l==rl else None),
    ('op','-',('num','*','op')):lambda l,rl,rr:((AST_Node(Symbol(str(eval(rl.symbol.value)-1))),l,Symbol('*')) if l==rr else None),
    (('op','*','num'),'+','op'):lambda ll,lr,r:((AST_Node(Symbol(str(eval(lr.symbol.value)+1))),r,Symbol('*')) if r==ll else None),
    (('num','*','op'),'+','op'):lambda ll,lr,r:((AST_Node(Symbol(str(eval(ll.symbol.value)+1))),r,Symbol('*')) if r==lr else None),
    (('op','*','num'),'-','op'):lambda ll,lr,r:((AST_Node(Symbol(str(eval(lr.symbol.value)-1))),r,Symbol('*')) if r==ll else None),
    (('num','*','op'),'-','op'):lambda ll,lr,r:((AST_Node(Symbol(str(eval(ll.symbol.value)-1))),r,Symbol('*')) if r==lr else None),
    ('num','*',('num','*','op')):lambda l,rl,rr:(AST_Node(Symbol(str(eval(l.symbol.value+'*'+rl.symbol.value)))),rr,Symbol('*')),
    ('num','*',('op','*','num')):lambda l,rl,rr:(AST_Node(Symbol(str(eval(l.symbol.value+'*'+rr.symbol.value)))),rl,Symbol('*')),
    (('num','*','op'),'*','num'):lambda ll,lr,r:(AST_Node(Symbol(str(eval(r.symbol.value+'*'+ll.symbol.value)))),lr,Symbol('*')),
    (('op','*','num'),'*','num'):lambda ll,lr,r:(AST_Node(Symbol(str(eval(r.symbol.value+'*'+lr.symbol.value)))),ll,Symbol('*')),    
    ('var','+',('num','*','var')):lambda l,rl,rr:((AST_Node(Symbol(str(eval(rl.symbol.value)+1))),l,Symbol('*')) if l==rr else None),
    ('var','-',('num','*','var')):lambda l,rl,rr:((AST_Node(Symbol(str(eval(rl.symbol.value)-1))),l,Symbol('*')) if l==rr else None),
    (('num','*','var'),'+','var'):lambda ll,lr,r:((AST_Node(Symbol(str(eval(ll.symbol.value)+1))),r,Symbol('*')) if r==lr else None),
    (('num','*','var'),'-','var'):lambda ll,lr,r:((AST_Node(Symbol(str(eval(ll.symbol.value)-1))),r,Symbol('*')) if r==lr else None),
    ('num','*',('num','*','var')):lambda l,rl,rr:(AST_Node(Symbol(str(eval(l.symbol.value+'*'+rl.symbol.value)))),rr,Symbol('*')),
    (('num','*','var'),'*','num'):lambda ll,lr,r:(AST_Node(Symbol(str(eval(r.symbol.value+'*'+ll.symbol.value)))),lr,Symbol('*')),
    (('var','^','num'),'^','num'):lambda ll,lr,r:(ll,AST_Node(Symbol(str(eval(r.symbol.value+'*'+lr.symbol.value)))),Symbol('^')),
    (('op','^','num'),'^','num'):lambda ll,lr,r:(ll,AST_Node(Symbol(str(eval(r.symbol.value+'*'+lr.symbol.value)))),Symbol('^')),
    (('num','*','var'),'*','var'):lambda ll,lr,r:(ll,AST_Node(Symbol('^'),lr,AST_Node(Symbol('2'))),Symbol('*')),
    }



_opt_rules3={
    (('num','*','var'),'+',('num','*','var')):lambda ll,lr,rl,rr:(AST_Node(Symbol(str(eval(ll.symbol.value+'+'+rl.symbol.value)))),rr,Symbol('*')),
    (('num','*','var'),'-',('num','*','var')):lambda ll,lr,rl,rr:(AST_Node(Symbol(str(eval(ll.symbol.value+'-'+rl.symbol.value)))),rr,Symbol('*')),
    (('var','^','num'),'/',('var','^','num')):lambda ll,lr,rl,rr:(ll,AST_Node(Symbol(str(eval(lr.symbol.value+'-'+rr.symbol.value)))),Symbol('^')),
    (('op','*','num'),'+',('op','*','num')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(lr.symbol.value+'+'+rr.symbol.value)))),ll,Symbol('*')) if ll==rl else None),
    (('num','*','op'),'+',('num','*','op')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(ll.symbol.value+'+'+rl.symbol.value)))),lr,Symbol('*')) if lr==rr else None),
    (('op','*','num'),'-',('op','*','num')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(lr.symbol.value+'-'+rr.symbol.value)))),ll,Symbol('*')) if ll==rl else None),
    (('num','*','op'),'-',('num','*','op')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(ll.symbol.value+'-'+rl.symbol.value)))),lr,Symbol('*')) if lr==rr else None),
    }



_jump_table={
    'sin':lambda x:AST_Node(Symbol('cos'),None,x),
    'cos':lambda x:AST_Node(Symbol('minus'),None,AST_Node(Symbol('sin'),None,x)),
    'tan':lambda x:AST_Node(Symbol('/'),AST_Node(Symbol('1')),AST_Node(Symbol('^'),AST_Node(Symbol('cos'),None,x),AST_Node(Symbol('2')))),
    'log':lambda x:AST_Node(Symbol('/'),AST_Node(Symbol('1')),x),
    '*':lambda l,s,r:AST_Node(Symbol('+'),AST_Node(Symbol('*'),l,s.right),AST_Node(Symbol('*'),r,s.left)),
    '+':lambda l,s,r:AST_Node(Symbol('+'),l,r),
    '-':lambda l,s,r:AST_Node(Symbol('-'),l,r),
    '/':lambda l,s,r:AST_Node(Symbol('/'),AST_Node(Symbol('-'),AST_Node(Symbol('*'),l,s.right),AST_Node(Symbol('*'),r,s.left)),AST_Node(Symbol('^'),s.right,AST_Node(Symbol('2')))),
    '^':lambda l,s,r:AST_Node(Symbol('+'),AST_Node(Symbol('*'),r,AST_Node(Symbol('*'),s,AST_Node(Symbol('log'),None,s.left))),\
                                              AST_Node(Symbol('*'),AST_Node(Symbol('*'),l,AST_Node(Symbol('^'),s.left,AST_Node(Symbol('-'),s.right,AST_Node(Symbol('1'))))),s.right)),
    }


class Symbol(object):
    def __init__(self,value,type='unknown',p=0):
        self.value=value
        if type=='unknown':
            try:
                num=eval(value)
                if num==0:
                    self.type='0'
                elif num==1:
                    self.type='1'
                else:
                    self.type='num'
            except:
                if value in _operators or value in _functions:
                    self.type='op'
                else:
                    self.type=type
        else:
            self.type=type
        self.precedence=p
        if self.type=='op':
            self.precedence=_precedence[value]

    def __eq__(self,another):
        return self.value==another.value and self.type==another.type
    
    def __str__(self):
        return '({})[{}]{}'.format(self.type,self.precedence,self.value)

class AST_Node(object):
    def __init__(self,value,left=None,right=None):
        debug_data,new_debug_data='',''
        if _DEBUG:
            debug_data='{} {} {}'.format(left.get_full_exp() if left else 'None',value,right.get_full_exp() if right else 'None')
        self.left,self.right,self.symbol=self.opt(value,left,right)
        self.min_p=self.symbol.precedence if self.symbol.precedence else 999
        if left and left.min_p and left.min_p<self.min_p:
            self.min_p=left.min_p
        if right and right.min_p and right.min_p<self.min_p:
            self.min_p=right.min_p;

        if _DEBUG:
            new_debug_data='{} {} {}'.format(left.get_full_exp() if left else 'None',value,right.get_full_exp() if right else 'None')
            if debug_data!=new_debug_data:
                print('before',debug_data)
                print('after',new_debug_data)
            else:
                print(debug_data)
        

    def opt(self,value,left,right):
        if left and right:
            lt,rt,st=left.symbol.type,right.symbol.type,value.value
            if any(lt==i for i in ['0','1','num']) and any(rt==i for i in ['0','1','num']):
                temp=eval(left.symbol.value+value.value+right.symbol.value)
                if temp>=0:
                    left,right,value=None,None,Symbol(str(temp))
                else:
                    left,right,value=None,AST_Node(Symbol(str(abs(temp)))),Symbol('minus')
            elif (lt,st,rt) in _opt_table:
                left,right,value=_opt_table[(lt,st,rt)](left,right)
            if left and right and right.left and right.right:
                rlt,rrt,lt=right.left.symbol.type,right.right.symbol.type,left.symbol.type
                if (lt,st,(rlt,right.symbol.value,rrt)) in _opt_rules2:
                    res=_opt_rules2[(lt,st,(rlt,right.symbol.value,rrt))](left,right.left,right.right)
                    if res:
                        left,right,value=res
            if left and right and left.left and left.right:
                llt,lrt,rt=left.left.symbol.type,left.right.symbol.type,right.symbol.type
                if ((llt,left.symbol.value,lrt),st,rt) in _opt_rules2:
                    res=_opt_rules2[((llt,left.symbol.value,lrt),st,rt)](left.left,left.right,right)
                    if res:
                        left,right,value=res
            if left and right and left.left and left.right and right.left and right.right:
                lt,rt=left.symbol.type,right.symbol.type
                ll,lr,rl,rr=left.left.symbol.type,left.right.symbol.type,right.left.symbol.type,right.right.symbol.type
                if ((ll,left.symbol.value,lr),value.value,(rl,right.symbol.value,rr)) in _opt_rules3:
                    res=_opt_rules3[((ll,left.symbol.value,lr),value.value,(rl,right.symbol.value,rr))](left.left,left.right,right.left,right.right)
                    if res:
                        left,right,value=res
        return left,right,value


    

    def travel(self,level=0):
        if self.left:
            self.left.travel(level+1)
        print(level*' '+str(self.symbol))
        if self.right:
            self.right.travel(level+1)



    def get_lambda(self):
        exp=self.get_full_exp(True)
        return lambda *kwargs:eval(exp)

    def get_full_exp(self,python_exp=False):
        left,right='',''
        sp=self.symbol.precedence
        if self.left:
            lsp=self.left.min_p
            left=self.left.get_full_exp()
            if lsp and lsp<sp:
                left='('+left+')'
        if self.right:
            rsp=self.right.min_p
            right=self.right.get_full_exp()
            if (rsp and rsp<sp) or self.symbol.value in _functions:
                right='('+right+')'

        v=self.symbol.value
        if v=='minus':
            v='-'
        elif v=='plus':
            v=''
        if python_exp:
            if self.symbol.type=='math_const':
               v='math.'+v 
            elif v=='^':
                v='**'
            elif v in _functions:
                v='math.'+v
        return left+v+right
    
    def get_derivative(self):
        left_d,right_d=None,None
        if self.left:
            left_d=self.left.get_derivative()
        if self.right:
            right_d=self.right.get_derivative()
        return self.inner_derivative(left_d,right_d)

    def inner_derivative(self,ld,rd):
        if not ld and not rd:
            return AST_Node(Symbol('1')) if self.symbol.type=='var' else AST_Node(Symbol('0'))
        elif not ld and rd:
            return AST_Node(Symbol('*'),_jump_table[self.symbol.value](self.right),rd)
        else:
            return _jump_table[self.symbol.value](ld,self,rd)

    def __eq__(self,another):
        return self.symbol==another.symbol and self.left==another.left and self.right==another.right

class derivator(object):
    def __init__(self,*args,**kwargs):
        assert all(not _symboldict_reserved in i for i in args),"any word contains '{}' cannot be a vaild variable name".format(_symboldict_reserved)
        assert all(not _symboldict_reserved in i for i in kwargs),"any word contains '{}' cannot be a vaild variable name".format(_symboldict_reserved)
        self.vars=[i for i in args]
        self.exps={i:kwargs[i] for i in kwargs}
        self.symboldict={}
        self.de_var=None
        self.stored_derivative=None

    def calc_derivative(self,**kwargs):
        if self.stored_derivative:
            return self.stored_derivative(**kwargs)
        else:
            raise ValueError

    def symboldict_add(self,value):
        key=_symboldict_reserved+str(len(self.symboldict)+1)
        self.symboldict[key]=value
        return key

           
    def build_AST(self,str_exp,de_var):
        tempRPN=self.generate_RPN(str_exp,de_var)
        stack=[]
        last=None
        for i in tempRPN:
            if i.type!='op':
                stack.append(AST_Node(i))
            else:
                temp=stack.pop()
                op=i.value
                if op=='minus':
                    last=AST_Node(i,None,temp)
                elif op=='plus':
                    last=temp
                elif op in _operators:
                    last=AST_Node(i,stack.pop(),temp)
                elif op in _functions:
                    last=AST_Node(i,None,temp)
                stack.append(last)
        return last    

    def generate_RPN(self,str_exp,de_var):
        stack=[]
        final_stack=[]
        i=0
        unknown_char=''
        lock_unknown=False
        while i<len(str_exp):
            func_flag=False
            char=str_exp[i]
            if (char=='-' or char=='+') and ((i>1 and str_exp[i-1]=='(') or i==0):
                char='minus' if char=='-' else 'plus'
            else:
                for k in _functions:
                    if str_exp[i:i+len(k)]==k:
                        char=k
                        i+=len(k)-1
                        func_flag=True
                        break
            if char.isdigit():
                end=i+1
                while end<len(str_exp) and (str_exp[end].isdigit() or str_exp[end]=='.'):
                    end+=1
                temp=str_exp[i:end]
                final_stack.append(Symbol(temp))
                i=end
            elif char=='%':
                i+=1
                for k in _math_const:
                    if str_exp[i:i+len(k)]==k:
                        final_stack.append(Symbol('%'+k,'math_const'))
                        break
                i+=1
            else:
                flag=False
                if str_exp[i:i+len(de_var)]==de_var:
                    final_stack.append(Symbol(de_var,'var',800))
                    flag=True
                if not flag:
                    for k in self.exps:
                        if str_exp[i:i+len(k)]==k:
                            final_stack.extend(self.generate_RPN(self.exps[k]))
                            flag=True
                            break
                if not flag:
                    if char=='(':
                        stack.append(Symbol(char))
                    elif char==')':
                        while stack[-1].value!='(':
                            final_stack.append(stack.pop())
                        stack.pop()
                    elif func_flag or char in _operators:
                        while len(stack) and _precedence[stack[-1].value]>=_precedence[char]:
                            final_stack.append(stack.pop())
                        stack.append(Symbol(char,'op'))
                    else:
                        for k in self.vars:
                            if str_exp[i:i+len(k)]==k:
                                final_stack(Symbol(k,'var_num'))
                                flag=True
                                break
                        if not flag:
                            raise SyntaxError
                i+=1
        stack.reverse()
        final_stack.extend(stack)
        return final_stack


a=derivator('x')
b='log(%e*x^4/(x-4)^6)'
print(a.build_AST('x^x^x','x').get_derivative().get_full_exp())


