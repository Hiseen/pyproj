def swap(array,a,b):
    if(id(array[a])==id(array[b])):
        return
    array[a]^=array[b]
    array[b]^=array[a]
    array[a]^=array[b]


def quicksort(array,start,end):
    if(end<=start):
        return
    j=partsort(array,start,end)
    quicksort(array,start,j-1)
    quicksort(array,j+1,end)
    
def partsort(array,start,end):
    i=start
    j=end+1
    c=array[i]
    while(True):
        i+=1
        while(array[i]<c):
            if(i==end):
                break
            i+=1
        j-=1    
        while(c<array[j]):
            if(j==start):
                break
            j-=1
        if(i>=j):
            break;
        swap(array,i,j)
    swap(array,j,start)
    return j



def entropysort(array,start,end):
    if(start>end):
        return 
    left=start
    right=end
    c=array[left]
    now=left
    while(now<=right):
        if(array[now]<c):
            swap(array,now,left)
            now+=1
            left+=1
        else:
            if(array[now]>c):
                swap(array,now,right)
                right-=1
            else:
                now+=1
    entropysort(array,start,left-1)
    entropysort(array,right+1,end)

def shellsort(array):
    N=len(array)
    h=1
    while(h<N/3):
        h=3*h+1
    while(h>=1):
        for i in range(h,N):
            j=i
            while(j>=h and array[j]<array[j-h]):
                swap(array,j,j-h)
                j-=h
        h=int(h/3)

def merge(array,copy,start,mid,end):
    for k in range(start,end+1):
        copy[k]=array[k]
    i=start
    j=mid+1
    for k in range(start,end+1):
        if(i>mid):
            array[k]=copy[j]
            j+=1
        else:
            if(j>end):
                array[k]=copy[i]
                i+=1
            else:
                if(copy[j]<copy[i]):
                    array[k]=copy[j]
                    j+=1
                else:
                    array[k]=copy[i]
                    i+=1

def msort(array,copy,start,end):
    if(start>=end):
        return
    mid=int(start+(end-start)/2);
    msort(array,copy,start,mid)
    msort(array,copy,mid+1,end)
    merge(array,copy,start,mid,end)



def mergesort(array):
    copy=array[:]
    msort(array,copy,0,len(array)-1)



def sort(num):
    import random
    a=[]
    switch={
        1:lambda a:quicksort(a,0,len(a)-1),
        2:lambda a:entropysort(a,0,len(a)-1),
        3:lambda a:shellsort(a),
        4:lambda a:mergesort(a)
         }
    for i in range(10):
        a.append(random.randint(0,10))
    print(a)
    (switch.get(num))(a)
    print(a)




class TreeNode:
    def __init__(self,data,left,right):
        self.data=data
        self.left=left
        self.right=right





















