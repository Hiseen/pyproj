
def check_core(types,args):
    if not types:
        return []
    elif isinstance(types,dict):
        for i in types.keys():
            k=args.find(' ') if args.find(' ')!= -1 else None
            tempres=check_core(i,args[:k])
            if tempres:
                tempres2=check_core(types[i],args[k:].strip())
                if tempres2!=None:
                    return tempres+tempres2
                else:
                    return None
    elif isinstance(types,tuple):
        res=None
        for i in types:
            try:
                if res!=None:
                    temp=i(res)
                else:
                    k=args.find(' ')
                    if k!=-1:
                        temp=i(args[:k])
                    else:
                        temp=i(args)
                if not isinstance(temp,bool):
                    res=temp
                elif not temp:
                    return None
            except Exception as e:
                print(e)
                return None
        return [res]
    elif isinstance(types,list):
        result=[]
        for i in types:
            r=check_core(i,args)
            if r!=None:
                result+=r
                args=args.split(maxsplit=len(r))[-1]
            else:
                return None
        return result
    else:
        try:
            return [types(args)]
        except:
            if types==args or types==args.upper():
                return [args]
            return None
            



def check_type(types,errormessage='ERROR'):
    while True:
        args=input()
        result=check_core(types,args)
        if result!=None:
            return result
        print(errormessage)
    



print(check_type({'STEPS':None,'TOTALDISTANCE':None,'TOTALTIME':None,'LATLONG':None,'ELEVATION':None}))






