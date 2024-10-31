import sys
from time import sleep, time
import json
import os
from io import StringIO
import ftplib, socket, ssl
from ftplib import error_perm
import threading
import shutil, math, json
import queue

class Testfunc(threading.Thread):
    name = 'testfunc'
    timestamp = 0
    res_list = []

    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name=name

    def get(self):
        return self.res_list

    def run(self):
        while True:
            if self.timestamp == 0:
                self.timestamp = time()
            else:
                t_now = time()
                t_dif = t_now-self.timestamp
                print('%s-%s, %10.10f ------ %10.10f'%(__name__,self.name, t_dif,t_now))
                self.res_list.append(t_now)
                self.timestamp = t_now
            sleep(1)

class prod(threading.Thread):
    def run(self):
        global cnt
        while True:
            if con.acquire():
                print('prod-acq:',cnt)
                if cnt > 700:
                    con.wait()
                    print('prod-wait')
                else:
                    cnt = cnt+100
                    msg=self.name + ' prod 100, cnt = ' + str(cnt)
                    print(msg)
                    con.notify()
                    print('prod-notify')

                con.release()
                print('prod-release')
                sleep(0.3)

class consum(threading.Thread):
    def run(self):
        global cnt
        while True:
            if con.acquire():
                print('consum-acq:',cnt)
                if cnt<100:
                    con.wait()
                    print('consum-wait')
                else:
                    cnt = cnt -13
                    msg = self.name+'consum 13,cnt = ' +str(cnt)
                    print(msg)
                    con.notify()
                    print('consum-notify')

                con.release()
                print('consum-release')
                sleep(1)

cnt=500
con=threading.Condition()

def main():
    # cli()
    # tf_1=Testfunc(name='hello_test_1')

    # tf_1.setDaemon(True)
    # tf_1.start()
    # sleep(5)
    # print(tf_1.get())


    p=prod()
    p.start()

    c=consum()
    c.start()

    sys.exit(0)


if __name__ == '__main__':
    main()
