import queue as O000O00O00OO0OO00 ,threading as OOO00OOOOOOOO0O0O #line:1
import time as O0O00O000O00O000O #line:2
def test_aaa ():#line:3
    __OO0O0OOOOOO0O0O0O =OOO00OOOOOOOO0O0O .Event ()#line:4
    __OO0O0OOOOOO0O0O0O .set ()#line:5
    __O000O0OO00OOO00OO =OOO00OOOOOOOO0O0O .Event ()#line:6
    __O000O0OO00OOO00OO .set ()#line:7
    def OOOO0OOOOOO0O0000 ():#line:10
        while __O000O0OO00OOO00OO .isSet ():#line:11
            __OO0O0OOOOOO0O0O0O .wait ()#line:12
            print (1 )#line:13
            O0O00O000O00O000O .sleep (1 )#line:14
    print ('2秒暂停')#line:17
    for OOO00O00OO0O00O0O in range (1 ):#line:18
        print (OOO00O00OO0O00O0O )#line:19
        OO000O000O00O0O0O =OOO00OOOOOOOO0O0O .Thread (target =OOOO0OOOOOO0O0000 )#line:20
        OO000O000O00O0O0O .start ()#line:22
    O0O00O000O00O000O .sleep (2 )#line:23
    print ('2秒后重新开始')#line:24
    __OO0O0OOOOOO0O0O0O .clear ()#line:25
    O0O00O000O00O000O .sleep (2 )#line:26
    print ('restart')#line:27
    print ('2秒后停止')#line:28
    O0O00O000O00O000O .sleep (2 )#line:30
    __OO0O0OOOOOO0O0O0O .set ()#line:32
    __O000O0OO00OOO00OO .clear ()
#e9015584e6a44b14988f13e2298bcbf9

