#!/usr/bin/env python3

import socket

class iMatic():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.head = b'\xFD\x02\x20'
        self.tail = b'\x5D'

    def connect(self):
        #http://stackoverflow.com/questions/16772465/how-to-use-socket-in-python-as-a-context-manager
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host,self.port))
        return s

    def changeState(self, relay, state):
        #http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
        msg = self.head + relay + state + self.tail
        s = self.connect()
        s.sendall(msg)
        ret = s.recv(1024)
        s.close()
        return ret

    def relayOn(self, relay):
        return self.changeState(bytes(chr(int(relay)), 'UTF-8'), b'\x01')

    def relayOff(self, relay):
        return self.changeState(bytes(chr(int(relay)), 'UTF-8'), b'\x00')

if __name__ == "__main__":
    import sys

    host = '192.168.1.4'
    port = 30000

    iM = iMatic(host, port)

    if sys.argv[2] == '1':
        iM.relayOn(sys.argv[1])
    else:
        iM.relayOff(sys.argv[1])
