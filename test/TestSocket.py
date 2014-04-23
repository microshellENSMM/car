from Socket import *
import socket

# Call back methode
def updateSocket(tab) :
		print tab
		if tab[0] == 1:
				resume = False
# Try Singleton patern
server = Server(2014)
server2 = Server(2014)
print server.id(), server2.id()
# Add call back method like listener
server.addListener(updateSocket)

# setup cient connection
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(('127.0.0.1', 2014))
resume = True
while resume :
		mes = input("> ")
		connection.send(mes.encode())



server.close()
