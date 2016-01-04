import threading
import socket
import os
from datetime import datetime
BUF_SIZE = 2048

cacheName =  []
cacheValue = []

class Respon(threading.Thread):
    def __init__(self, newConn, newAddr,nama):
        self.newConn=newConn
        self.newAddr = newAddr
        self.nama = nama
        self.log = str( datetime.now().strftime('%H:%M:%S')) + ' from ' + self.nama
        threading.Thread.__init__(self)

    def openfile(self,nama):
        if nama not in cacheName :
            print 'DIFFERENT!'
            readValue =  open(nama).read()
            cacheName.append ( nama )
            cacheValue.append ( readValue )
            return readValue
        else :
            indexa = cacheName.index(nama)
            return cacheValue[indexa]

    def routeConnection(self, request):
        splits = request.split(" ")
        try :
            temp = splits[1]
            pecahkan = pecahkan[1::]
        except :
            temp = ''
        finally :
            pecahkan = temp
        responses = 'HTTP/1.1 200 OK\r\n\r\n'


        if( pecahkan == '' ) :
            responses = responses + self.openfile( str('404.jpg'))
        # url matches 'x'.jpg
        elif os.path.isfile(str(pecahkan)+'.jpg'):
            responses = responses + self.openfile( str(pecahkan)+'.jpg')
        else :
            responses = responses + self.openfile( str('404.jpg'))


        self.log = self.log + ' Req : ' + str(pecahkan)

        self.newConn.send(responses)

    def run(self):
        response = ''
        while True:
            # receiving data
            received = self.newConn.recv( BUF_SIZE )
            if received:
                response = response + received

                if(response.endswith("\r\n\r\n")):
                    # print 'CRLF detected'
                    self.routeConnection(received)
                    break
            else :
                break
        self.log = self.log + ' finished.'
        print self.log

        # not closed to create persistent connection
        self.newConn.close()


#Deklarasi kelas
class Server(threading.Thread):
    def __init__(self):
        HOST = raw_input('Masukkan IP (default: localhost)')
        if HOST == '' : HOST = 'localhost'
        PORT = raw_input('Masukkan Port ( 900 + input anda ; default 9000)')
        if PORT == '' : PORT = 9000
        elif PORT != '' : PORT = 9000 + int(PORT)

        self.addr = (str(HOST), int(PORT))
        self.servsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.servsocket.bind(self.addr)

        threading.Thread.__init__(self)
        print ('Server is running on %s port %s ' %self.addr)

    def run(self):
        self.servsocket.listen(1)
        while True:
            self.newConn , self.connAddress = self.servsocket.accept()
            #handling
            newConnection = Respon(self.newConn, self.connAddress, str(self.connAddress[0]) + ' <' + str(self.connAddress[1]) + '>')
            newConnection.start()


newServ = Server()
newServ.start()
