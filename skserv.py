#!/usr/bin/python
# -*- coding: utf-8
# Simple multithreading socket server v 1.5
# max buffer 16k, encode/decode utf8
# separator \t
import string
import sys
import socket
import threading
import time

msg_ok='ok'
msg_err='err'
separator="\t"

MAX_BUFFER=16000
CONNECT_TIMEOUT=8

class SockSrv:
    def __init__(self,ip,port,maxc):
        if ip=='':
            ip=''
        self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soc.bind((ip,port))
        self.soc.listen(maxc)
        self.maxc=maxc
        self.connections=0

    def start(self):
        print "skserv.start"
        while 1:
            (conn,addr) = self.soc.accept()
            if self.maxc<=self.connections:
                conn.send(msg_err)
                conn.close()
            else:
                self.connections=self.connections+1
                thr = CThread(self,conn)
                thr.start()
                conn.send(msg_ok)
        print 'skserv.close'
        self.soc.close()

    def process(self,ct,arr):
        pass


class CThread(threading.Thread):
    def __init__(self,socksrv,c):
        self.MAXSIZE = MAX_BUFFER
        threading.Thread.__init__(self)
        self.conn = c
        self.stopIt=False
        self.arr=[]
        self.socksrv=socksrv

    def mrecv(self):
        data = self.conn.recv(self.MAXSIZE)
        #data=data.decode('utf8')
        s = data.rstrip("\r\n")
        self.arr = s.split(separator)
        return data

    def run(self):
        print "skserv.connect"
        while not self.stopIt:
            data = self.mrecv()
            if not data:
                self.stopIt=True
                break
            #print data
            self.socksrv.process(self,self.arr)
        self.conn.close()
        self.socksrv.connections=self.socksrv.connections-1
        print "skserv.disconnect [%s]" % (self.socksrv.connections)

    def msend(self,msg):
        if len(msg)<=self.MAXSIZE and len(msg)>0:
            try:
                m=msg.encode('utf8')
            except:
                m=msg
            msg=m

            self.conn.send(msg)


class SockClient:
    def __init__(self,ip,port):
        self.MAXSIZE = MAX_BUFFER
        if ip=='':
            ip='127.0.0.1'
        #print ip+":"+str(port)
        self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soc.settimeout(CONNECT_TIMEOUT)
        try:
            self.soc.connect((ip,port))
        except:
            self.soc = None


    def mrecv(self):
        data = self.soc.recv(self.MAXSIZE)
        #data=data.decode('utf8')
        s = data.rstrip("\r\n")
        self.arr = s.split(separator)
        return data

    def msend(self,msg):
        if len(msg)<=self.MAXSIZE and len(msg)>0:
            self.soc.send(msg)

    def run(self):
        pass

    def close(self):
        try:
            self.soc.close()
        except:
            pass

#if len(sys.argv) > 1:
#    ip=sys.argv[1]
#else:
#    ip=''
#
#if len(sys.argv) > 2:
#    port=sys.argv[2]
#else:
#    port=7171
#
#try:
#    srv=SockSrv(ip,port,1)
#    print "starting socket server"
#    srv.start()
#except:
#    print "error socket server"
#

