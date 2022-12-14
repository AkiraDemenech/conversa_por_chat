
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
		connection = tcp()
		connection.socket.connect(address)
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


protocol = tcp
TIMEOUT = 10 + (15 * (protocol == udp))
BURST = 4
SIZE = 500

class main:

	def __init__ (self):
		self.main = tkinter.Tk()
		self.active = True
		self.main.title(protocol.__name__.upper() + ' chat (File transfer)') # mudando o título da janela principal 

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

		self.burst = BURST
		self.burst_ack_timeout = TIMEOUT #ms
		self.burst_ack = {}

		

		
		print('Chatting with',self.address,'(File transfer)')
		

	def send (self):	
	#	self.main.msg.send.config(state=tkinter.DISABLED)
		
		filename = self.main.msg.text.get().strip()
		if len(filename):
			name = filename.split('/')[-1].split('\\')[-1]
			queue = []
			with open(filename, 'rb') as file:				
				self.main.bind('<Return>', print)
				c = 0
				while True:
					c += 1
					head = (f'{hex(c)[2:]}/{name}\\').encode()

					if len(head) < SIZE:
						body = file.read(SIZE - len(head))
					else:	
						body = file.read(SIZE)
						print('File too large:\t',c,name)															
						return
					
					# último pacote do arquivo
					if len(body) + len(head) < SIZE:
						queue.append((c,name,('|'*(SIZE-len(body)-len(head))).encode() + head + body))
						break
					queue.append((c, name, head + body))																	 
					 	
						

			while len(self.sending) > 0:		
				print('Waiting',len(self.sending))
				time.sleep(len(self.sending)/(1 + len(self.sending)))
				
			# primeiro pacote do arquivo
			pre = f'{hex(self.burst)[2:]}/{hex(SIZE)[2:]}/{hex(len(queue))[2:]}|/'
			pos = '/' + name + '\\'
			queue.insert(0, (False, name, (pre + ('0' * (SIZE - len(pre) - len(pos))) + pos).encode()))

			print(name,len(queue),SIZE)
			self.sending.extend(queue)	

			threading.Thread(target=self.send_file).start()
			
			
			self.main.msg.text.delete(0,tkinter.END)
			paragraph = tkinter.Frame(self.main.chat)
			t = time.localtime()[:5]
			if t != self.last:
				if t[2] != self.last[2]:
					tkinter.Label(paragraph, text='%02d/%02d/%d' %t[2::-1]).pack()
				self.last = t
				tkinter.Label(paragraph, text='%02d:%02d' %t[3:]).pack()								
			tkinter.Label(paragraph, text=filename).pack(side=tkinter.RIGHT)	
			paragraph.pack(fill=tkinter.X) 

	#	self.main.msg.send.config(state=tkinter.ACTIVE)	
		self.main.bind('<Return>', self.main.msg.send.function)

	def send_file (self):
		
		lost = []
		burst = []
		self.burst_ack.clear()
		ti = time.time()

		while len(self.sending):
			c, name, msg = self.sending.pop(0)			
			self.connection.sendall(msg)	
			print('Sending:\t', name, c)
			
			burst.insert(0, (name, c))
			self.sending_files[(name, c)] = msg

			if (c % self.burst) and len(self.sending):
				# espera entre envio pacotes para garantir integridade na leitura do header
				self.connection.sleep() 
				continue

			print('Burst:\t',len(self.sending),'left')

			for t in range(self.burst_ack_timeout):
				if c in self.burst_ack:
					print('Burst ACK (',len(self.burst_ack),'):\tpackage',self.burst_ack[c],'\t',t,'ms')
					break 
				time.sleep(1 / 1000)
			else:
				print('Burst ACK timeout',t)
				for name, c in burst:
					self.sending.insert(0,(c,name,self.sending_files[(name,c)]))
				lost.extend(burst)
					
				
				self.burst_ack_timeout <<= (self.burst_ack_timeout < 100) # dobramos o timeout, caso seja lentidão na rede	
			burst.clear()	

		tf = time.time()		

		print(locale.format_string('%.6f', tf - ti, grouping=True),'s\t', (locale.format_string('%.6f', (len(lost) + c + 1) * SIZE / ((tf - ti) * (2**17)), grouping=True) + ' total Mb/s'))	
		print(locale.format_string('%d', len(lost) + c + 1, grouping=True), 'sent (' + locale.format_string('%d', c + 1, grouping=True), 'unique packages),')
		print(locale.format_string('%d', len(lost), grouping=True), 'lost (' + locale.format_string('%d', len(set(lost)), grouping=True), 'unique packages):')
		
		for f, l in lost:
			print(f, '\t', l)



	def send_burst_ack (self, file, package):		

		self.connection.sendall(('/-a/' + hex(len(self.files[file]['data']) - 1)[2:] + '/' + hex(package)[2:] + '/\\').zfill(SIZE).encode())

	def mainloop (self, msg):	

		f = ''
		j = k = n = m = i = b = False
				
		while len(msg) > i:
			c = msg[i]
			i += 1	
			if c == 124:	#|
				if not b:
					print('EOF (size)')
					b = True
			elif c == 47:	#/	
				j = k	
				k = m
				m = n
				n = int(f, 16)
				f = ''
			elif c == 92:	#\
				break
			else:
				f += chr(c)
		else:		
			# suposto nome do arquivo, número do pacote, quantos pacotes faltam até o último e se tem essa informação (é pacote de tamanho), bytes desse pacote lidos até agora, último e penúltimo número, pacotes por rajada (janela) e bytes por pacote
			print('ERROR\t',repr(f),n,m,b,i,j,k) 

				 
		# file name, package number, last package number if it has this information, header size (bytes), burst size (packages), package size (bytes) 	
		print(f, n, m, b, i, j, k) 
		if not len(f):	
			if k == -10: 
				self.burst_ack[m] = n
				print('Burst ACK received\t-a', m, n)
			return

				
		ti = time.time()
						
		if not f in self.files:
					
			print('Starting',f,'\t','%d-%d-%d_%d-%d-%d' %time.localtime(ti)[:6])
			self.files[f] = {
									'size':None,
									'last':False,
									'start':ti,'end':ti,
									'repeated': [],
									'done':False,
									'data':{}
							}
							
		if n in self.files[f]['data']: 
			self.files[f]['repeated'].append((n, self.files[f]['last']))
			
		else:											

			self.files[f]['data'][n] = msg[i:]	
			self.files[f]['last'] = n	

			if len(self.files[f]['data']) % self.burst == 1:

				self.send_burst_ack(f, n)
				print('Sending burst ACK')
				
		if b or not n:
			self.files[f]['size'] = n + m + 1
			print('Size:',self.files[f]['size'],len(self.files[f]['data']))
			if k:
				global SIZE
				SIZE = k
				if j:
					self.burst = j
					print('Burst size:',j)
				print('Package size:',SIZE)
			if self.files[f]['done'] and n <= self.burst:
				self.files[f]['done'] = False
				self.files[f]['data'].clear()
				self.files[f]['start'] = ti
				self.files[f]['repeated'].clear()	
				return 
						
		if len(self.files[f]['data']) == self.files[f]['size']:
			self.send_burst_ack(f, n)
			print('Sending final burst ACK')
			dt = ti - self.files[f]['start']
			sz = self.files[f]['size'] * SIZE
			print('Saving',f,'\t','%d-%d-%d_%d-%d-%d' %time.localtime(ti)[:6],'\t',locale.format_string('%.6f', dt, grouping=True),'s\n', locale.format_string('%d', sz, grouping=True), 'bytes (' + locale.format_string('%.3f', sz / (1024**2), grouping=True),'MB =',locale.format_string('%.3f', sz / (1024 * 128), grouping=True),'Mb)\t', (locale.format_string('%.6f', sz / (1024 * 128 * dt), grouping=True) + ' successful Mb/s') if dt else '')
			repeated = len(self.files[f]['repeated'])		
			print(locale.format_string('%d', repeated + self.files[f]['size'], grouping=True), 'packages received:')
			print(locale.format_string('%d', self.files[f]['size'], grouping=True), 'unique packages,')
			print(locale.format_string('%d', repeated, grouping=True), 'repeated packages:')
			for n, l in self.files[f]['repeated']: 
				print('\t', n, '\t', l)

			self.files[f]['end'] = ti	

			if self.files[f]['done']:	
				print('File already saved.')
				return
					
			with open(f, 'wb') as file:
				k = list(self.files[f]['data'])
				k.sort()
				for c in k:
					file.write(self.files[f]['data'][c])
							
			print(f, 'saved.\n\r')	
			self.files[f]['done'] = True					

			paragraph = tkinter.Frame(self.main.chat)
			paragraph.pack(fill=tkinter.X)
			tkinter.Label(paragraph, text=f).pack(side=tkinter.LEFT)	
			t = time.localtime()[:5]
			if t != self.last:					
				if self.last[2] != t[2]:
					tkinter.Label(paragraph, text='%02d/%02d/%d' %t[2::-1]).pack()					
				tkinter.Label(paragraph, text='%02d:%02d' %t[3:]).pack()
				self.last = t		
			
	def destroy (self):
		self.active = False
		self.main.destroy()

print('.') 
# ponto final avisa o fim das definições

if __name__ == '__main__':		
	main().start()	



