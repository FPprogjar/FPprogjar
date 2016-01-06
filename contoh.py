import asyncore, socket, urllib2,threading
import Queue as q
import numpy as np
import pprint as pp
from datetime import datetime

BUF_SIZE = 2048
# server1 =

class Workers():
    def __init__ (self) :   # IP (string) ,
                            # PORT (int),
                            # WEIGHT (int)
                            # used (INT: default 0)
        self.serverAddr   = [[ 'http://10.151.36.103', 9000 ],
                             [ 'http://10.151.36.102', 9000 ],
                             [ 'http://10.151.36.105', 9000 ],
                             [ 'http://10.151.36.104', 9000 ],
                             [ 'http://10.151.34.34', 9000 ] ]

        self.arrayServer = np.array ([   [ 17000 , 1],
                                         [ 18000 , 1],
                                         [ 32000 , 1],
                                         [ 24000 , 1],
                                         [ 9000 , 1]] )

    def getServer(self) :
        #find the maximum weight divided to request added
        newArray = [ zi/yi for zi,yi in zip ( self.arrayServer[:,0] , self.arrayServer[:,1] ) ]
        maxIndex = newArray.index( max(newArray) )

        winningServer = self.arrayServer[maxIndex]
        # winningServer[0] = winningServer[0] - 1
        winningServer[1] = winningServer[1] + 1

        return self.serverAddr[maxIndex]

class HTTPHandler(asyncore.dispatcher):
    def __init__(self, client, addr, server, slave):
        asyncore.dispatcher.__init__(self, client)
        self._SERVER = str(slave[0])
        self._SERVERPORT = int(slave[1])
        self.log = '[' + str( datetime.now().strftime('%H:%M:%S')) + '] ' + str(addr)

    def handle_read(self):
        data = self.recv( BUF_SIZE )

        if data :
            splits = data.split(" ")
            try :
                temp = splits[1]
                pecahkan = pecahkan[1::]
            except :
                temp = ''
            finally :
                pecahkan = temp
            responses = 'HTTP/1.1 200 OK\r\n\r\n'
            # print pecahkan

            servers = self._SERVER + ':' + str(self._SERVERPORT) + '/' + pecahkan

            self.log = self.log + 'forwarded to ' + servers
            # print servers

            z =  urllib2.urlopen(servers).read()
            self.send( responses + z )

            print self.log

            self.close()


class HTTPServer(asyncore.dispatcher):
    def __init__(self):

        HOST = raw_input('Masukkan IP (default: localhost)')
        if HOST == '' : HOST = 'localhost'
        PORT = raw_input('Masukkan Port (default:8080)')
        if PORT == '' : PORT = 8080
        self.slave = Workers()
        self.addr = (str(HOST), int(PORT))

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.set_reuse_addr()
        self.bind(self.addr)
        self.listen(100000)
        print 'Load Balancer now Live on port %d' % self.addr[1]

    def handle_accept(self):
        (client, addr) = self.accept()
        HTTPHandler(client, addr, self, self.slave.getServer())


server = HTTPServer()
asyncore.loop()
