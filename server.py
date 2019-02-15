import socket
from threading import Thread
import threading, time
import random
import pickle
clientList = []

playerList = []


def clientThread(c, addr):
	connection = True
	#Now send back the player their ID
	message = pickle.dumps(["setID", "server", random.randint(100,999)])
	c.send(message)
	while connection == True:
		try:
			#Recieve 1024 of bytes of data from client. The data comes in encoded
			data = c.recv(4096)
			if not data:
				break
			print("From connected user:", addr, ":", data)
			print("Sending to all clients:", data)
			broadcastAll(data)
		except ConnectionResetError as e:
			print("Connection Closed:", addr)
			clientList.remove(c)
			connection = False
			#print("Connection Closed:", c, addr)
			#No data so close connection

def broadcastAll(data):
	for client in clientList:
		try:
			client.send(data)
		except ConnectionResetError as e:
			print("ConnectionResetError:", client)
			clientList.remove(client)

def Main():
	host = "127.0.0.1"
	port = 5000
	#Create the TCP socket 
	s  = socket.socket()
	#Bind the socket to the  host and port
	s.bind((host, port))
	#Listen to 1 connection
	s.listen(2)
	while True:
		print("Threads: ", threading.active_count())
		#Wait and accept the connection and store the socket object of the client and address
		c, addr = s.accept()
		clientList.append(c)
		print("Received a connection from:", c, str(addr))
		print("Current clientList len:", len(clientList))
		t = Thread(target=clientThread, args=(c, addr))
		t.start()

if __name__ == "__main__":
	Main()