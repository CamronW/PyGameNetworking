import socket
import time
import select
import pygame
import pickle
from threading import Thread
pygame.init()

class Client():
	def __init__(self):
		self.serverHost = "127.0.0.1"
		self.serverPort = 5000
		self.s = None
	def connect(self):
		self.s = socket.socket()
		self.s.connect((self.serverHost, self.serverPort))
		self.s.setblocking(0)
	def messageServer(self, message):
		self.s.send(message)
	def recv(self):
		data = self.s.recv(4096)
		#print("Recieved from server:", data)
		game.handleServerMessage(data)
	def close(self):
		self.s.close()

def serverThread(client):
	client.connect()
	print("Client connected")
	while True:
		#Check if there's data ready
		ready = select.select([client.s], [], [], 0.1)
		if ready[0]:
			client.recv()

	s.close()
	
class Player():
	def __init__(self, posX, posY):
		self.posX = posX
		self.posY = posY
		self.width = 50
		self.height = 50
		self.movX = 0
		self.movY = 0
		self.velocity = 3
		self.playerID = ""
		self.clientID = ""
	def setMov(self, movX, movY):
		self.movX = movX
		self.movY = movY
	def updatePos(self):	
		self.posX = self.posX + (self.movX * self.velocity)
		self.posY = self.posY + (self.movY * self.velocity)


class Game():
	def __init__(self):
		self.client = None
		self.serverT = None
		self.fps = 60
		self.fpsClock = pygame.time.Clock()
		self.width = 640
		self.height = 480
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.player = Player(self.width/2, self.height/2)
		self.client = None
		self.otherPlayers = []

	def startGame(self):
		#Setup network thread and client
		self.client = Client()
		serverT = Thread(target=serverThread, args=(self.client,)).start()
		#//TODO: It waits 1 sec for a connection there's a better way to do this
		time.sleep(1)


	def drawScreen(self):
		#Draw other players
		for player in self.otherPlayers:
			pygame.draw.rect(self.screen, (255,0,0), (player.posX, player.posY, player.width, player.height))
			
		#Draw player rect
		pygame.draw.rect(self.screen, (0,255,255), (self.player.posX, self.player.posY, self.player.width, self.player.height))
		pygame.display.flip()

	def handlePlayerMovement(self):
		#Handle 8 directional movement
		keys_pressed = pygame.key.get_pressed()
		movX = 0
		movY = 0
		if keys_pressed[pygame.K_w]:
			movY = -1
		elif keys_pressed[pygame.K_s]:
			movY = 1
		else:
			movY = 0
		if keys_pressed[pygame.K_d]:
			movX = 1
		elif keys_pressed[pygame.K_a]:
			movX = -1
		else:
			movX = 0
		self.player.setMov(movX, movY)
		self.player.updatePos()

	def handleServerMessage(self, message):
		#The message format is: name, clientID, object
		message = pickle.loads(message)
		if message[0] == "setID":
			self.player.clientID = message[2]
			print(f"Recieved 'setID' from Client Number: {message[1]} -> {message[2]}")
		elif message[0] == "playerObject":
			#print(f"Recieved 'playerObject' from Client Number: {message[1]} -> {message[2]}")
			self.handlePlayerObjectRecieved(message)
		else: 
			print("Weird mesage:", message)

	def handlePlayerObjectRecieved(self, message):
		#print(f"Recieved 'playerObject' from Client Number: {message[1]} -> {message[2]}")
		messageClientID = message[1]
		messagePlayerObject = message[2]
		print(self.otherPlayers)
		if messageClientID == self.player.clientID:
			pass
		else: 
			#Now we know the data is coming from a different client
			#Remove duplicate object so it isn't interacted  with multiple times
			for otherPlayer in self.otherPlayers:
				if otherPlayer.clientID == messagePlayerObject.clientID:
					self.otherPlayers.remove(otherPlayer)
			self.otherPlayers.append(messagePlayerObject)
			#print(messageClientID, messagePlayerObject.posX, messagePlayerObject.posY)

	def loop(self):
		self.screen.fill((0,0,0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		self.fpsClock.tick(self.fps)
		self.handlePlayerMovement()
		self.drawScreen()
		#message = input("-> ")
		toDump = ["playerObject", self.player.clientID, self.player]
		message = pickle.dumps(toDump)
		self.client.messageServer(message)

def Main():
	game.startGame()
	while True:
		game.loop()
if __name__ == "__main__":
	game = Game()
	Main()