import threading
import socket
import sys

server =[]
#array untuk menampung daftar server yang ada
max = 20000
banyak = []
#array untuk menampung jumlah koneksi pada setiap server



n = 0

def giliran(n) :
	lala= n % 5 # lala adalah variable untuk menentukan index yang akan digunakan untuk menentukan server
	return lala

def hitung(a) :
	#coba adalah variable yang menunjukkan ketersidiaan server dalam menerima koneksi baru
	if banyak[a] < max :
	  banyak[a] = banyak[a] + 1
	  coba = 1
	else :
	  coba = 0
	return coba

def cekserver() : #mengecek jumlah server yang belum penuh
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
