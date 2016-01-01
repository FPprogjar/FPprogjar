import threading
import socket
import sys

server =[]
flag = []
max = 25000
banyak = []
n = 0

def giliran(n) :
	lala= n % 5
	return lala

def hitung(a) :
	if flag[a] < 20000 :
	  banyak[a] = banyak[a] + 1
	  flag[a] = 0
	  coba = 1
	else :
	  coba = 0
	return coba

def cekserver() :
	count = 0
	for x in range (0,5) :
		if hitung[x]==1 :
		   count=count+1
	return count

if __name__ == '__main__':
	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 5555)
	my_socket.bind(server_address)
	my_socket.listen(1)
	while(True):
		connection, client_address = my_socket.accept()
		while(True):
			data=connection.recv(2048)
			print data
			if data:
				ip = giliran(n)
				cek = hitung(ip)
				if cek == 1 :
				   #connect ke server
				else :
					yeye=cekserver()
					if yeye > 0 :
						for x in range (0,4):
							if hitung(x) == 1 :
							   ip = x
						   	break
						#connect ke server
					else :
						connection.send("Server Full")
					connection.close()

			break
	
