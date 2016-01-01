#! /usr/bin/env python3

import asyncore #https://docs.python.org/2/library/asyncore.html
import socket
import threading
import queue
import time

fqueue = queue.Queue()

class Handler(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.keep_reading = True

    def run(self):
        while self.keep_reading:
            if fqueue.empty():
                time.sleep(1)
            else:
                #PROCESS
    def stop(self):
        self.keep_reading = False


class Listener(asyncore.dispatcher): #http://effbot.org/librarybook/asyncore.htm
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))


    def handle_read(self):
        data = self.recv(40) #pretend it always waits for 40 bytes
        fqueue.put(data)

    def start(self):
        try:
            h = Handler()
            h.start()
            asyncore.loop()
        except KeyboardInterrupt:
            pass
        finally:
            h.stop() 
