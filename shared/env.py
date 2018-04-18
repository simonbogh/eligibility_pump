# Echo server

# Importing Libraries
import socket
import sys
import struct
import array

SIMULINK = "simulink"

class environment:
	def __init__(self, env_decider):
		self.env_decider = env_decider
        # Connection for sender socket
		self.sendConn = 0
		self.sendHost = 'localhost'  # Symbolic name meaning all available interfaces
		self.sendPort = 50000        # Arbitrary non-privileged port
		# Connection for receiver socket
		self.recvConn = 0
		self.recvHost = 'localhost'  # Symbolic name meaning all available interfaces
		self.recvPort = 50001        # Arbitrary non-privileged port
		self.last_data = 0
	
	# Creating server Socket
	def createServerSockets(self):
		
		# Calling socket creater methods
		self.createSendServerSocket()
		self.createRecvServerSocket()

	def createSendServerSocket(self):
		# Creating server Socket location
		serverSocketS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			serverSocketS.bind((self.sendHost, self.sendPort))
		except:
			print('Bind failed.')
			sys.exit()
		print ('Socket bind complete')
		# Enable listening
		serverSocketS.listen(1)
		print ('Socket now listening')
		
		# Wait for client connection
		print ('waiting 10 seconds for response from client at sender port ',self.sendPort)
		serverSocketS.settimeout(10)
		try:
			self.sendConn, addr = serverSocketS.accept()
		except socket.timeout:
			print('No connection, program terminated')
			sys.exit()
		print ('Connected by', addr,'on sender port',self.sendPort)
		
		
		# Create socket for receiving
		
		# Creating server Socket
	def createRecvServerSocket(self):
		# Creating server Socket location
		serverSocketR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			serverSocketR.bind((self.recvHost, self.recvPort))
		except:
			print('Bind failed.')
			sys.exit()
		print ('Socket bind complete')
		# Enable listening
		serverSocketR.listen(1)
		print ('Socket now listening')
		
		# Wait for client connection
		print ('waiting for response from client at receiver port ',self.recvPort)
		self.recvConn, addr = serverSocketR.accept()
		print ('Connected by', addr,'on receiver port',self.recvPort)
	
	def receiveState(self):
		# Receive state formed as binary array
		data = self.recvConn.recv(2048);
		# decode state
		if self.env_decider == SIMULINK:
			return self.decodeSimulinkState(data)
		else:
			return self.decodeMatlabState(data)
        
	def decodeMatlabState(self, data):
		# Unpack from hex (binary array) to double
		try:
			data = str(data)
			data = data.split(",")
			del data[0]
			del data[6]
			data = [float(i) for i in data]
		except: 
			data = self.last_data
        
		return data

	def decodeSimulinkState(self, data):
		# Unpack from hex (binary array) to double
		try:
			data = array.array('d',data)
		except: 
			data = self.last_data

		return data
		
	def sendAction(self, msg):
		msg = struct.pack("I",msg)
		self.sendConn.sendall(msg)#.encode('utf-8'))	