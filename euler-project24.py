def help_func(num):
    if num==1:
        return 1
    result=help_func(num-1)*num
    return result


print(help_func(1))
print(help_func(10))

def func(num):
    l=[i for i in range(10)]
    size=9
    temp=num-1
    result=[]
    while size:
        fact=help_func(size)
        if fact!=0:
            index=temp//fact
            temp=temp%fact
        else:
            index=0
            temp=0
        result.append(l[index])
        l.remove(l[index])
        size-=1
    result.append(l[0])
    return result

print(func(1000000))
