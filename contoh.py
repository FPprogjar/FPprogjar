import asyncore, socket, urllib2
from datetime import datetime



_SERVER = 'http://localhost'
_SERVERPORT = 9000
BUF_SIZE = 1024
# server1 =

class HTTPHandler(asyncore.dispatcher):
    def __init__(self, client, addr, server):
        asyncore.dispatcher.__init__(self, client)
        self.log = '[' + str( datetime.now().strftime('%H:%M:%S')) + '] From ' + str(addr)

    def handle_read(self):
        data = self.recv(1024)

        if data :
            splits = data.split(" ")
            pecahkan = splits[1]
            pecahkan = pecahkan[1::]
            responses = 'HTTP/1.1 200 OK\r\n\r\n'
            # print pecahkan

            servers = _SERVER + ':' + str(_SERVERPORT) + '/' + pecahkan
            self.log = self.log + 'forwarded to ' + servers
            # print servers

            z =  urllib2.urlopen(servers).read()
            self.send( responses + z )

            self.log = self.log + ' Finished'
            print self.log


            # self.end_headers()
            self.close()

    def handle_close(self):
        pass

class HTTPServer(asyncore.dispatcher):
    def __init__(self):

        HOST = raw_input('Masukkan IP (default: localhost)')
        if HOST == '' : HOST = 'localhost'
        PORT = raw_input('Masukkan Port (default:8080)')
        if PORT == '' : PORT = 8080

        self.addr = (str(HOST), int(PORT))

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        self.set_reuse_addr()
        self.bind(self.addr)
        self.listen(100000)
        print 'Load Balancer now Live on port %d' % self.addr[1]

    def handle_accept(self):
        (client, addr) = self.accept()
        HTTPHandler(client, self.addr, self)

if __name__ == '__main__':

    server = HTTPServer()
    asyncore.loop()
