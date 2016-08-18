import re
import math


_precedence={'(':0,')':0,
             '-':1,'+':1,
             '*':2,'/':2,
             'plus':3,'minus':3,'sin':3,'cos':3,'tan':3,'log':3,'sqrt':3,
             '^':4
             }

_operators='-+*/^minusplus'

_functions=['sin','cos','tan','log','sqrt']

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
    ('var','^','0'):lambda x,y:(None,None,Symbol('1')),# alert! var may equal to 0 !
    ('var','/','1'):lambda x,y:(x.left,x.right,x.symbol),
    ('op','^','1'):lambda x,y:(x.left,x.right.x.symbol),
    ('op','^','0'):lambda x,y:(None,None,Symbol('1')), # alert! exp may equal to 0 !
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
    ('-1','*','op'):lambda x,y:(None,y,Symbol('minus')),
    ('op','*','-1'):lambda x,y:(None,x,Symbol('minus')),
    ('-1','*','var'):lambda x,y:(None,y,Symbol('minus')),
    ('var','*','-1'):lambda x,y:(None,x,Symbol('minus')),
    ('op','/','op'):lambda x,y:((None,None,Symbol('1')) if x==y else None),
    ('op','-','op'):lambda x,y:((None,None,Symbol('0')) if x==y else None),
    (None,'log','math_const'):(lambda x,y:(None,None,Symbol('1')) if y.symbol.value=='%e' else None),
    
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
    ('1','/',('var','/','op')):lambda l,rl,rr:(rr,rl,Symbol('/')),
    ('1','/',('op','/','var')):lambda l,rl,rr:(rr,rl,Symbol('/')),
    ('1','/',('op','/','op')):lambda l,rl,rr:(rr,rl,Symbol('/')),
    (('op','+','op'),'/','op'):lambda ll,lr,r:(AST_Node(Symbol('/'),ll,r),AST_Node(Symbol('/'),lr,r),Symbol('+')),
    (('op','-','op'),'/','op'):lambda ll,lr,r:(AST_Node(Symbol('/'),ll,r),AST_Node(Symbol('/'),lr,r),Symbol('-')),
    (('op','*','op'),'/','op'):lambda ll,lr,r:(lr.left,lr.right,lr.symbol) if ll==r else (ll.left,ll.right,ll.symbol) if lr==r \
                                                else (AST_Node(Symbol('/'),ll,r),lr,Symbol('*')) if ll.related(r) else (AST_Node(Symbol('/'),lr,r),ll,Symbol('*')),
    (None,'minus',(None,'minus','op')):lambda l,rl,rr:(rr.left,rr.right,rr.symbol),
    }



_opt_rules3={
    (('num','*','var'),'+',('num','*','var')):lambda ll,lr,rl,rr:(AST_Node(Symbol(str(eval(ll.symbol.value+'+'+rl.symbol.value)))),rr,Symbol('*')),
    (('num','*','var'),'-',('num','*','var')):lambda ll,lr,rl,rr:(AST_Node(Symbol(str(eval(ll.symbol.value+'-'+rl.symbol.value)))),rr,Symbol('*')),
    (('var','^','num'),'/',('var','^','num')):lambda ll,lr,rl,rr:(ll,AST_Node(Symbol(str(eval(lr.symbol.value+'-'+rr.symbol.value)))),Symbol('^')),
    (('op','^','num'),'/',('op','^','num')):lambda ll,lr,rl,rr:((ll,AST_Node(Symbol(str(eval(lr.symbol.value+'-'+rr.symbol.value)))),Symbol('^')) if ll==rl else None),
    (('op','*','num'),'+',('op','*','num')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(lr.symbol.value+'+'+rr.symbol.value)))),ll,Symbol('*')) if ll==rl else None),
    (('num','*','op'),'+',('num','*','op')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(ll.symbol.value+'+'+rl.symbol.value)))),lr,Symbol('*')) if lr==rr else None),
    (('op','*','num'),'-',('op','*','num')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(lr.symbol.value+'-'+rr.symbol.value)))),ll,Symbol('*')) if ll==rl else None),
    (('num','*','op'),'-',('num','*','op')):lambda ll,lr,rl,rr:((AST_Node(Symbol(str(eval(ll.symbol.value+'-'+rl.symbol.value)))),lr,Symbol('*')) if lr==rr else None),
    (('op','/','op'),'*',('op','/','op')):lambda ll,lr,rl,rr:(AST_Node(Symbol('/'),ll,rr),AST_Node(Symbol('/'),rl,lr),Symbol('*')),
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
                elif num==-1:
                    self.type='-1'
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
        self.count=1
        if self.left:
            if self.left.min_p and self.left.min_p<self.min_p:
                self.min_p=self.left.min_p
            self.count+=self.left.count
        if self.right:
            if self.right.min_p and self.right.min_p<self.min_p:
                self.min_p=self.right.min_p
            self.count+=self.right.count
        

        
        if _DEBUG:
            new_debug_data='{} {} {}'.format(self.left.get_full_exp() if self.left else 'None',self.symbol,self.right.get_full_exp() if self.right else 'None')
            if debug_data!=new_debug_data:
                print('before',debug_data)
                print('after',new_debug_data)
            else:
                print(debug_data)

    def __str__(self):
        return str(self.symbol)


    def opt(self,value,left,right):
        if value.value=='minus':
            if right.symbol.type!='var' and right.symbol.type!='op':
                return None,None,Symbol('-'+right.symbol.value)
        if right:
            lt,rt,st=left.symbol.type if left else None,right.symbol.type,value.value
            if any(lt==i for i in ['0','1','num','-1']) and any(rt==i for i in ['0','1','num','-1']):
                temp=eval(left.symbol.value+value.value+right.symbol.value)
                left,right,value=None,None,Symbol(str(temp))
            elif (lt,st,rt) in _opt_table:
                if _DEBUG:
                    print((lt,st,rt))
                res=_opt_table[(lt,st,rt)](left,right)
                if res and self.sum_count(*res)<self.sum_count(left,right,value):
                    left,right,value=res
        if right and right.right:
            st=value.value
            rlt,rrt,lt=right.left.symbol.type if right.left else None,right.right.symbol.type,left.symbol.type if left else None
            if _DEBUG:
                print((lt,st,(rlt,right.symbol.value,rrt)))
            if (lt,st,(rlt,right.symbol.value,rrt)) in _opt_rules2:
                res=_opt_rules2[(lt,st,(rlt,right.symbol.value,rrt))](left,right.left,right.right)
                if res and self.sum_count(*res)<self.sum_count(left,right,value):
                    left,right,value=res
        if left and right and left.right:
            st=value.value
            llt,lrt,rt=left.left.symbol.type if left.left else None,left.right.symbol.type,right.symbol.type
            if _DEBUG:
                print(((llt,left.symbol.value,lrt),st,rt))
            if ((llt,left.symbol.value,lrt),st,rt) in _opt_rules2:
                res=_opt_rules2[((llt,left.symbol.value,lrt),st,rt)](left.left,left.right,right)
                if res and self.sum_count(*res)<self.sum_count(left,right,value):
                    left,right,value=res
        if left and right and left.left and left.right and right.left and right.right:
            lt,rt=left.symbol.type,right.symbol.type
            ll,lr,rl,rr=left.left.symbol.type,left.right.symbol.type,right.left.symbol.type,right.right.symbol.type
            if _DEBUG:
                print(((ll,left.symbol.value,lr),value.value,(rl,right.symbol.value,rr)))
            if ((ll,left.symbol.value,lr),value.value,(rl,right.symbol.value,rr)) in _opt_rules3:
                res=_opt_rules3[((ll,left.symbol.value,lr),value.value,(rl,right.symbol.value,rr))](left.left,left.right,right.left,right.right)
                if res and self.sum_count(*res)<self.sum_count(left,right,value):
                    left,right,value=res
        return left,right,value



    def related(self,another):
        if self==another:
            return True
        if self.symbol.value==another.symbol.value:
            v=self.symbol.value
            if v=='^':
                if self.right.symbol.type==another.right.symbol.type=='num' and self.left==another.left:
                    return True
            elif v=='*':
                if any(self.left==i for i in (another.left,another.right)) or any(self.right==i for i in (another.left,another.right)):
                    return True
            elif v=='/':
                if self.right==another.right or self.left==another.left:
                    return True
        return False
                

    def sum_count(self,left,right,value):
        res=1
        if left:
            res+=left.count
        if right:
            res+=right.count
        return res
        
            
            

    def travel(self,level=0):
        if self.left:
            self.left.travel(level+1)
        print(level*' '+str(self.symbol))
        if self.right:
            self.right.travel(level+1)

    def __iter__(self):
        return self.iter_func()

    def iter_func(self):
        yield self
        if self.left:
            for i in self.left:
                yield i
        if self.right:
            for i in self.right:
                yield i

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
               v='math.'+v if v[0]!='-' else '-math.'+v[1:]
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
        if self.symbol.value=='minus':
            return AST_Node(Symbol('minus'),None,self.right.get_derivative())
        if not ld and not rd:
            return AST_Node(Symbol('1')) if self.symbol.type=='var' else AST_Node(Symbol('0'))
        elif not ld and rd:
            return AST_Node(Symbol('*'),_jump_table[self.symbol.value](self.right),rd)
        else:
            return _jump_table[self.symbol.value](ld,self,rd)

    def __eq__(self,another):
        return self.symbol==another.symbol and self.left==another.left and self.right==another.right

class derivator(object):
    def __init__(self):
        self.stored_derivative=None

    def calc_derivative(self,**kwargs):
        if self.stored_derivative:
            return self.stored_derivative(**kwargs)
        else:
            raise ValueError


    def get_derivative(self,str_exp,var,itertime=1,**kwargs):
        assert isinstance(itertime,int) and itertime>=1
        result=self.build_AST(str_exp,var,kwargs).get_derivative().get_full_exp()
        for i in range(itertime-1):
            result=self.build_AST(result,var,kwargs).get_derivative().get_full_exp()
        return result
        
           
    def build_AST(self,str_exp,var,exps):
        tempRPN=self.generate_RPN(str_exp,var,exps)
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
                elif op=='sqrt':
                    last=AST_Node(Symbol('^'),temp,AST_Node(Symbol('-1')))
                elif op in _operators:
                    last=AST_Node(i,stack.pop(),temp)
                elif op in _functions:
                    last=AST_Node(i,None,temp)
                stack.append(last)
        return last    

    def generate_RPN(self,str_exp,var,exps):
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
                if str_exp[i:i+len(var)]==var:
                    final_stack.append(Symbol(var,'var',800))
                    flag=True
                if not flag:
                    for k in exps:
                        if str_exp[i:i+len(k)]==k:
                            final_stack.extend(self.generate_RPN(exps[k]))
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
                        raise SyntaxError
                i+=1
        stack.reverse()
        final_stack.extend(stack)
        return final_stack

if __name__=='__main__':
    a=derivator()
    b='log(%e*x^4/(x-4)^6)'
    print(a.get_derivative('1/(1+%e^(-x))','x'))

