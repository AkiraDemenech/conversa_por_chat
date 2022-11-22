
print(end='\n.') # o primeiro ponto avisa que o programa abriu e está carregando
from audioop import add
import socket # Internet Socket API 

print(end='.') # o segundo ponto avisa a abertura da segunda dependência
import threading  
import tkinter 
import time

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

print(end='.') # o terceiro ponto avisa a definição das classes 
LOG = 'ip_port.log'
SEP = '\t'

class socket_interface:

	socket = address = dest = None
	conn_callback = msg_callback = print

	def connection_callback (self, callback):
		self.conn_callback = callback

	def message_callback (self, callback):
		self.msg_callback = callback	

	def dest_address (self, dest):		
		self.dest = dest
		

	def connection (self, conn):	
		self.socket = conn

	def bind (self, address):
		if address == None:
			return 
		self.address = address
		self.socket.bind(self.address)

	def listen (self):	
		
		return

	def sleep (self):

		return	

	def mainloop (self):		
		
		return	

	def start (self):	

		self.mainloop()

	 	

class tcp (socket_interface):
	def __init__ (self, address = None, connection = None):
		super().connection(connection if connection != None else socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		super().bind(address)	
		
	def connect (self, address):
		connection = tcp(connection = self.socket.connect(address))
		connection.dest_address(address)
		return connection

	def sendall (self, data):	
		self.socket.sendall(data)

	def listen (self):	

		while True:

			self.socket.listen()
			connection, address = self.socket.accept()

			connection = tcp(connection = connection)
			connection.dest_address(address)

			
			self.conn_callback(connection, address)

	def mainloop (self):		

		while True:

				
			self.msg_callback(self.socket.recv(SIZE))

	def sleep (self):		

		time.sleep(1 / 100)

class udp (socket_interface): 
	def __init__ (self, address = None, connection = None):
		super().connection(connection if connection != None else socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
		super().bind(address)
		self.connections = {}
	
	def connect (self, address):
		
		connection = udp(connection = self.socket)
		#connection.address = self.address
		connection.dest_address(address)
		
		
		self.connections[address] = connection
		return connection

	

	def sendall (self, data): # envia os bytes para o endereço conectado		
		
		c = 0
		while c < len(data):
			c += self.socket.sendto(data[c:], self.dest)	

	def listen (self):	

		while True:

			try:
				msg, address = self.socket.recvfrom(SIZE)
			except ConnectionResetError:				
				self.socket.close()
				self.connection(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) 	
				self.bind(self.address)
				for c in self.connections:
					self.connections[c].connection(self.socket)
				print('Reset connection')	
				continue
			if not address in self.connections:
				
												
				self.conn_callback(self.connect(address), address)
				
				

			self.connections[address].msg_callback(msg)	


protocol = udp
TEST_TEXT = 'teste de rede *2022*'
TEST_TIME = 20 
TEST_TURNS = 4
SIZE = 500

MSG_TEXT = TEST_TEXT * (SIZE / len(TEST_TEXT)).__ceil__()

class main:

	def __init__ (self):
		self.main = tkinter.Tk()
		self.active = True
		self.main.title(protocol.__name__.upper() + ' chat (Speed test)') # mudando o título da janela principal 

	def start (self):	
		self.main.address = tkinter.Frame(self.main)
		self.main.address.pack(fill=tkinter.X)
		
		self.main.address.container = tkinter.Frame(self.main.address)
		self.main.address.container.pack()

		tkinter.Label(self.main.address.container, text='IP').pack(side=tkinter.LEFT)

		self.main.address.ip = tkinter.Entry(self.main.address.container)
		self.main.address.ip.pack(side=tkinter.LEFT)

		tkinter.Label(self.main.address.container, text='port:').pack(side=tkinter.LEFT)

		self.main.address.port = tkinter.Entry(self.main.address.container)
		self.main.address.port.pack(side=tkinter.LEFT)

		self.main.address.start = tkinter.Button(self.main.address.container, text='Start', command=self.server)
		self.main.address.start.pack(side=tkinter.LEFT)

		try:
			with open(LOG,'r') as log:
				address = log.read().split(SEP)
				print(address)

				if len(address) >= 2:
					self.main.address.port.insert(0,address[1].strip())

				if len(address) >= 1:
					self.main.address.ip.insert(0,address[0].strip())	

		except FileNotFoundError:	
			pass

		self.main.bind('<Return>', lambda e: self.main.address.start.invoke())
		self.main.mainloop()

	def server (self):

		try:	

			self.address = self.main.address.ip.get().strip(), int(self.main.address.port.get())

			if self.address[1] <= 1023:
				print('Não insira uma porta privilegiada')
				return

			if self.address[1] > 65535:
				print('Insira uma porta de até 2 bytes')
				return 
			
			


			self.socket = protocol(self.address)
			self.socket.connection_callback(self.connect)
			threading.Thread(target=self.socket.listen).start()
			

			with open(LOG,'w') as log:
				print(*self.address,sep=SEP,file=log)							

			self.main.address.start.config(command=self.client,text='Connect')
			tkinter.Label(self.main.address, text='Listening:\n' + str(self.address)).pack()	
			print('Server address:\t',self.address)

			
		except ValueError:

			print('Insira um inteiro válido na porta')	

	def connect (self, connection, address):		

		chat(self.main, connection, address, 'from')

	def client (self):		

		try:
			address = self.main.address.ip.get().strip(), int(self.main.address.port.get())					
			print('Connecting to',address)
			chat(self.main, self.socket.connect(address), address, 'to')

		except ValueError:
			print('Corrija a porta para um inteiro válido')	

		

	def mainloop (self):	
		self.start()

class chat:

	def __init__ (self, m, c, a, l = ''):		

		self.main = tkinter.Toplevel(m)
		self.main.chat = tkinter.Frame(self.main)
		self.main.chat.pack(fill=tkinter.BOTH)
		
		self.main.msg = tkinter.Frame(self.main)
		self.main.msg.pack(side=tkinter.BOTTOM, fill=tkinter.X)

		self.main.msg.send = tkinter.Button(self.main.msg, text='Send', command=self.send)
		self.main.msg.send.pack(side=tkinter.RIGHT)
		self.main.msg.send.function = lambda e: self.main.msg.send.invoke()

		self.main.msg.text = tkinter.Entry(self.main.msg)
		self.main.msg.text.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

		

		self.files = {}
		self.sending_files = {}
		self.sending = []
		
		
		self.connection = c
		self.connection.message_callback(self.mainloop)
		threading.Thread(target=self.connection.mainloop).start()
		self.address = a
		self.active = True
		self.last = {2:None}

		self.main.bind('<Return>', self.main.msg.send.function)
		self.main.title(l + ' ' + str(a)) # mudando o título da conversa

		
		self.burst_ack = {}

		

		
		print('Chatting with',self.address,'(Speed test)')
		

	def send (self):	
		self.main.msg.send.config(state=tkinter.DISABLED)
		
		pacote = TEST_TEXT * (SIZE // len(TEST_TEXT))
		pacote += '\0' * (SIZE - len(pacote))

		# iniciar teste 

		self.main.msg.send.config(state=tkinter.ACTIVE)	
		self.main.bind('<Return>', self.main.msg.send.function)

	def send_test (self):
		
		ti = time.time()
		c = 0

		while True:
			tf = time.time()			
			if tf - ti >= TEST_TIME:	
				break
			
			c += 1 	

				
	def header (self, number = 0, finite_test = False, r = False):			

		


	def encode_in_bytes (self, n, end=b'\0'):	

		v = b = 0

		while n > 0:

			v = (v << 7) + (n % 128) + 128
			n >>= 7
			b += 1
		
		if b:
			return v.to_bytes(b, 'big') + end
		return (128).to_bytes(1, 'big') + end	

				
					

				 

				
						
					
							
			
	

	def mainloop (self, msg):	

		n = i = f = t = r = False
		v = []
				
		while len(msg) > f: 
			c = msg[f]
			
			if c:	
				n = (n << 7) + c - 128 
			else:	#\0	
				if i >= f:
					break # acaba com \0\0
				r = t	
				t = n

				v.append(n)
				n = False #ord(msg[i:f].decode()) - 128
				
				i = f + 1
			f += 1		
			
		else:		
			# número do pacote, número do teste, índices inicial e final de leitura do texto, lista de valores
			print('ERROR\t',n,t,i,f,v) 

				 
				
						


					
							

			
	def destroy (self):
		self.active = False
		self.main.destroy()

print('.') 
# ponto final avisa o fim das definições

if __name__ == '__main__':		
	main().start()	



