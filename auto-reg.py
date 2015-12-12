import urllib.parse
import requests
from bs4 import BeautifulSoup
from collections import namedtuple
import time

RegClass=namedtuple('RegClass','classlist isfinished')

def get_redirect(text):
    pos=text.find('url=')
    pos2=text[pos:].find('>')
    return text[pos+4:pos+pos2-1]



username=input('Please enter your UCI username: ')
password=input('Please enter your password: ')
listofclass=[]
while True:
    a=input("Please enter a class code or a range of class code, enter non-number for end:\n")
    if a.find('-')!=-1:
        b=a.split('-')
        flag=True
        if len(b)!=2:
            flag=False
        for i in b:
            try:
                int(i)
            except:
                flag=False
                break
        if flag:
            listofclass.append(RegClass([str(i) for i in range(int(b[0]),int(b[1])+1)],False))
    else:
        try:
            int(a)
            listofclass.append(RegClass([a],False))
        except:
            break
        
regdelay=int(input("Please enter a number stand for how many minutes for loop-register, 0 stand for no loop-register:\n"))          





page_status=0



def find_and_print_msg(text):
    pos=text.find('''<div class="WebRegErrorMsg">''')
    while True:
        pos2=pos+text[pos:].find('''</div>''')
        print(text[pos+28:pos2].strip())
        temp=text[pos2:].find('''<div class="WebRegErrorMsg">''')
        if temp==-1:
            break
        pos+=temp







def try_to_enroll(classcode,call):
    global page_status
    #enter enrollment website:
    postdata2='page=enrollQtrMenu&mode=enrollmentMenu&call={:4d}&submit=Enrollment+Menu'.format(call).replace(' ','0').encode()
    req3=s.post(webregurl,headers=header4,data=postdata2)
    #post enrollment form
    postdata3='page=enrollmentMenu&call={:4d}&button=Send+Request&mode=add&courseCode={:}&gradeOption=&varUnits=&authCode=&courseCode='.format(call,classcode).replace(' ','0').encode()
    req4=s.post(webregurl,headers=header4,data=postdata3)
    page_status='enrollmentMenu'
    if req4.text.find('you have added')==-1:
        find_and_print_msg(req4.text)
        print('enrollment for {:}... failure! try waitlist...\n'.format(classcode))
        #try to add the class to waitlist:
        postdata4='page=enrollmentMenu&mode=waitlistMenu&call={:4d}&submit=Go+to+Wait+List+Menu'.format(call).replace(' ','0').encode()
        req5=s.post(webregurl,headers=header4,data=postdata4)
        #post waitlist form:
        postdata5='page=waitlistMenu&call={:4d}&button=Send+Request&mode=add&courseCode={:}&gradeOption=&varUnits=&courseCode='.format(call,classcode).replace(' ','0').encode()
        req6=s.post(webregurl,headers=header4,data=postdata5)
        page_status='waitlistMenu'
        if req6.text.find('you have wait listed')==-1:
            find_and_print_msg(req6.text)
            print("waitlist for {:}... failure! try to enroll it next loop\n".format(classcode))
            return False
        else:
            print("waitlist for {:}... success!\n")
            return True
    else:
        print('enrollment for {:}... success!\n'.format(classcode))
        return True



username=urllib.parse.urlencode({'ucinetid':username})
password=urllib.parse.urlencode({'password':password})







#start loop-register
while True:
    #init
    s=requests.session()
    #login
    loginurl='http://webreg2.reg.uci.edu:8889/cgi-bin/wramia?page=startUp&call='
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Connection":"keep-alive",
    "Host":"login.uci.edu",
    "Referer":"http://webreg2.reg.uci.edu:8889/cgi-bin/wramia?page=startUp&call=",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
    }
    req1=s.get(loginurl,headers=header)
    nexturl=get_redirect(req1.text)
    header2={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Connection":"keep-alive",
    "Cache-Control":"max-age=0",
    "Content-Length":"325",
    "Content-Type":"application/x-www-form-urlencoded",
    "Host":"login.uci.edu",
    "Origin":"https://login.uci.edu",
    "Referer":nexturl,
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
        }

    postdata='referer=http%253A%252F%252Fwebreg2.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253DstartUp%2526call%253D&return_url=http%253A%252F%252Fwebreg2.reg.uci.edu%253A8889%252Fcgi-bin%252Fwramia%253Fpage%253Dlogin%253Fcall%253D0028&info_text=&info_url=&submit_type=&\
    {:}&{:}&login_button=Login'.format(username,password).encode()
    req=s.post(nexturl,headers=header2,data=postdata)
    nexturl=get_redirect(req.text)
    poscall1=nexturl.find('call=')
    call=nexturl[poscall1+5:poscall1+9]
    call=int(call)
    if s.cookies.get_dict()['ucinetid_auth']!='no_key':
        print('login complete!')
    else:
        print('login failure!')
        break


    #go to webreg:
    header3={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    #"Cookie":"_ga=GA1.2.148035365.1447662468;"+s.cookies.get_dict()['ucinetid_auth'],
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
        }
    req2=s.get(nexturl,headers=header3)
    header4={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    #"Cookie":"_ga=GA1.2.148035365.1447662468;"+s.cookies.get_dict()['ucinetid_auth'],
    "Host":"webreg2.reg.uci.edu:8889",
    "Origin":"http://webreg2.reg.uci.edu:8889",
    "Referer":"http://webreg2.reg.uci.edu:8889/cgi-bin/wramia",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
        }
    webregurl='http://webreg2.reg.uci.edu:8889/cgi-bin/wramia'

    #enrollment:
    for i in range(len(listofclass)-1,-1,-1):
        for j in listofclass[i].classlist:
            if try_to_enroll(j,call):
                listofclass[i]._replace(isfinished=True)
                break
        if listofclass[i].isfinished:
            listofclass.remove(listofclass[i])

    #logout
    print('logouting.....')
    logouturl="http://webreg2.reg.uci.edu:8889/cgi-bin/wramia?page=login?call={:4d}".format(call).replace(' ','0')
    header5={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"en-US,en;q=0.8",
    "Cache-Control":"max-age=0",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    #"Cookie":"_ga=GA1.2.148035365.1447662468;"+s.cookies.get_dict()['ucinetid_auth'],
    "Host":"webreg2.reg.uci.edu:8889",
    "Origin":"http://webreg2.reg.uci.edu:8889",
    "Referer":logouturl,
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36"
        }
    logoutdata='page={:}&mode=exit&call={:}&submit=Logout'.format(page_status,call).replace(' ','0').encode()
    logoutreq=s.post(logouturl,headers=header5,data=logoutdata)
    print(logoutreq.text)
    print('logout complete!')
    print('closing session...')
    s.close()
    print('session closed!')
    if len(listofclass)==0:
        break
    if regdelay:
        time.sleep(regdelay*60)
    else:
        break
    
print('You have enrolled/waitlisted all the classes!')

























