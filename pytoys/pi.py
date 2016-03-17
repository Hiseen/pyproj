def calcpi():
    res=0
    num=0
    gap=100
    res2=0
    count=0
    while(True):
        if(num%gap==0 and res and res2):
            str1=str(res*4)
            str2=str(res2*4)
            for i in range(count,len(str1)):
                if(str1[i]==str2[i]):
                   print(str1[i],end="")
                   count+=1
                   gap*=2
                else:
                   break
        res2=res
        res+=(-1 if (num-1)%2==0 else 1)*(1/(2*num+1))
        num+=1
    #print(res*4)

def trashsort(array):
    length=len(array)
    newarray=[0 for x in range(length)]
    for i in range(length):
        for j in range(length):
            if array[j]>i+1:
                newarray[i]+=1
    return newarray;

            
def printcode():
    import random
    while(True):
        print(random.randint(0,1),end="")



calcpi()














