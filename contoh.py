import asyncore, socket, urllib2



SERVER = 'http://localhost'
_SERVERPORT = 9000
BUF_SIZE = 1024
# server1 =

class HTTPHandler(asyncore.dispatcher):
    def __init__(self, client, addr, server):
        asyncore.dispatcher.__init__(self, client)

    def handle_read(self):
        data = self.recv(1024)

        if data :
            splits = data.split(" ")
            pecahkan = splits[1]
            pecahkan = pecahkan[1::]
            # print pecahkan

            servers = SERVER + ':' + str(_SERVERPORT) + '/' + pecahkan
            print servers
            # socket1.sendall("GET %s HTTP/1.0\n\n" %servers)
            self.send( urllib2.urlopen(servers).read() )


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
        print 'Request from %s:%s' % (self.addr[0], self.addr[1])
        HTTPHandler(client, self.addr, self)

if __name__ == '__main__':

    server = HTTPServer()
    asyncore.loop()
