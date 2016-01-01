import asyncore
import socket
import threading
import Queue as q
import time

connections = q.Queue()

class Handler(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.keep_reading = True

	def run(self):
		while self.keep_reading :
			if connections.empty():
				time.sleep(1)
			else :
				print "asfdasdf"
				#PROCESS
				#TODO

	def stop(self):
		self.keep_reading = False,

class Listener( asyncore.dispatcher ):
	def __init__(self) :
		host = 'localhost'
		port = 8080
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))

	def handle_read(self):
		data= self.recv(40)
		connections.put(data)

	def handle_read(self):
		print "asdfasdf"

	def start(self):
		try : # Error handling
			h = Handler()
			h.start()
			asyncore.loop()
		except KeyboardInterrupt :
			pass
		finally :
			h.stop()

dumplings = Listener()
dumplings.serve_forever()