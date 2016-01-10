from fractions import Fraction

def get():
    result=[]
    f=True
    while f:
        data=input()
        if data!='':
            try:
                result.append([Fraction(i) for i in data.split()])
            except:
                print('Error input')
        else:
            break
    if len(result)<len(result[0])-1:
        result+=[[Fraction(0) for i in range(len(result[0]))]for j in range(len(result[0])-1-len(result))]
    return result
        


def show(l):
    for i in range(len(l)):
        for j in range(len(l[i])):
            print('{:>6}'.format(str(l[i][j])),end=' ')
        print()
    print()






def calc(l,result):
    if not result:
        result=[None for i in range(len(l[0])-1)]
    #determine which two rows need to be calc:
    r1,r2,complexity,direction,finalcol,add=-1,-1,100000,1,0,False
    for col in range(len(l[0])-2):
        for i in range(len(l)):
            for j in range(i+1,len(l)):
                if l[i][col]!=0 and l[j][col]!=0 and any(l[i][:col])==any(l[j][:col])==False:
                    #print(l[i][col],l[j][col],l[i][:col],l[j][:col])
                    temp1,temp2=str(l[i][col]/l[j][col]),str(l[j][col]/l[i][col])
                    if temp1=='-1':
                        r1,r2,complexity,direction=i,j,0,0
                    elif complexity>len(temp1) or complexity>len(temp2):
                        r1,r2,complexity,direction=(i,j,len(temp1),-1) if len(temp1)<len(temp2) else (i,j,len(temp2),1)
                if direction==0:
                    break
            if direction==0:
                break
        finalcol=col
        if r2!=-1:
            break
    
    if r2!=-1:
        #print('r1:{},r2:{},direction:{}'.format(r1,r2,direction))
        if direction==-1:
            temp=l[r1][finalcol]/l[r2][finalcol]
            #print(temp)
            for i in range(len(l[0])-1,-1,-1):
                l[r1][i]-=l[r2][i]*temp
        elif direction==1:
            temp=l[r2][finalcol]/l[r1][finalcol]
            for i in range(len(l[0])-1,-1,-1):
                l[r2][i]-=l[r1][i]*temp
        else:
            for i in range(len(l[0])-1,-1,-1):
                l[r2][i]+=l[r1][i]
    else:
        #final output
        #print(result)
        for i in range(len(result)):
            if result[i]!=None:
                for k in range(len(l)):
                    if l[k][i]!=0 and k!=i:
                        l[k][-1]-=l[k][i]*result[i]
                        l[k][i]=0
        #show(l)
        for i in range(len(l)):
            if result[i]==None:
                finalrow,index=None,None
                for j in range(len(l[i])-1):
                    if l[i][j]!=0:
                        if index==None:
                            index=j
                            finalrow=i
                        else:
                            index=None
                            finalrow=None
                            break
                if index:
                    break
        #print(finalrow,index)
        l[finalrow][-1]/=l[finalrow][index]
        l[finalrow][index]=1
        result[index]=l[finalrow][-1]
        if finalrow!=index:
            l[finalrow],l[index]=l[index],l[finalrow]
    return l,result



mat=get()
result=None
while True if result==None else None in result:
    mat,result=calc(mat,result)
    show(mat)
        
            
                    
                    
                    
                
                    
            
    
    
    
    
    
