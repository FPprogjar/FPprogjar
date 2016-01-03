import threading
import socket
import os
from datetime import datetime
BUF_SIZE = 512

HOST = 'localhost'
PORT = 8080

class Respon(threading.Thread):
    def __init__(self, newConn, newAddr,nama):
        self.newConn=newConn
        self.newAddr = newAddr
        self.nama = nama
        self.log = str( datetime.now().strftime('%H:%M:%S')) + ' from ' + self.nama
        threading.Thread.__init__(self)

    def openfile(self,nama):
        ampas = open(nama)
        return ampas.read()

    def routeConnection(self, request):
        splits = request.split(" ")
        pecahkan = splits[1]
        pecahkan = pecahkan[1::]
        responses = 'HTTP/1.1 200 OK\r\n\r\n'


        if( str(splits[1]) == '/' ) :
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
                    self.routeConnection(received)
                    break
            else :
                break
        self.log = self.log + ' finished.'
        print self.log
        self.newConn.close()

#Deklarasi kelas
class Server(threading.Thread):
    def __init__(self):
        HOST = raw_input('Masukkan IP (default: localhost)')
        if HOST == '' : HOST = 'localhost'
        PORT = raw_input('Masukkan Port (default:80)')
        if PORT == '' : PORT = 8080

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
