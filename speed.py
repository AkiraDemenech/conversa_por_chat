
print(end='\n.') # o primeiro ponto avisa que o programa abriu e está carregando

import socket # Internet Socket API 

print(end='.') # o segundo ponto avisa a abertura da segunda dependência
import threading  
import tkinter 
import time
import math


import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

print(end='.') # o terceiro ponto avisa a definição das classes 
LOG = 'ip_port.log'
SEP = '\t'

SCALE_PREFIX = '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'


numf = lambda x: locale.format_string('%.3f' if type(x) == float and not x.is_integer() else '%d', x, grouping=True)
active = True

class socket_interface:

	socket = address = dest = None
	conn_callback = msg_callback = print
	connections = {}
	parent = None

	def connection_callback (self, callback):
		self.conn_callback = callback

	def message_callback (self, callback):
		self.msg_callback = callback	

	def dest_address (self, dest):		
		self.dest = dest
		

	def connection (self, conn):	
		self.socket = conn

	def close (self, dest):	
		if dest in self.connections: 
			print('Closing connection with',dest)
			self.connections.pop(dest)
		else:	
			print('Connection with',dest,'not found')

		if self.parent == None: 
			print('No parent found')
			return 

		if self.parent == self:
			print('Self-parenting')
			return 

		print('Closing @ parent')
		self.parent.close(dest)

	def bind (self, address):
		if address == None:
			return 
		self.address = address
		self.socket.bind(self.address)

	def listen (self):	
		
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
		print(address)
		connection = tcp()

		connection.parent = self
		connection.socket.connect(address)		
		connection.dest_address(address)
		
		return connection

	def sendall (self, data):	
		self.socket.sendall(data)

	def listen (self):	
		global active

		while active:

			self.socket.listen()
			connection, address = self.socket.accept()

			connection = tcp(connection = connection)
			connection.dest_address(address)
			connection.parent = self

			
			self.conn_callback(connection, address)

		print('Closing TCP listening loop')	

	def mainloop (self):		
		global active

		while active:

				
			self.msg_callback(self.socket.recv(SIZE))

		print('Closing TCP recv mainloop')	

	

class udp (socket_interface): 
	


	def __init__ (self, address = None, connection = None):
		super().connection(connection if connection != None else socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
		super().bind(address)
		
	
	def connect (self, address):
		
		connection = udp(connection = self.socket)
		
		connection.dest_address(address)
		connection.parent = self 
		
		self.connections[address] = connection
		return connection

	

	def sendall (self, data): # envia os bytes para o endereço conectado		
		
		c = 0
		while c < len(data):
			c += self.socket.sendto(data[c:], self.dest)	

	def listen (self):	
		global active

		while active:

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

		print('Closing UDP listening loop')	


protocol = tcp
TEST_TEXT = 'teste de rede *2022*'
TEST_TIME = 20 * 1000
TEST_TURNS = 2
SIZE = 500

TEST_ID = False 


#MSG_TEXT = (TEST_TEXT * math.ceil(SIZE / len(TEST_TEXT))).encode()

class main:

	def __init__ (self):
		self.main = tkinter.Tk()
		
		self.main.protocol('WM_DELETE_WINDOW', self.destroy)
		self.main.title(protocol.__name__.upper() + ' Speed test') # mudando o título da janela principal 

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
				print('Unavailable port')
				return

			if self.address[1] >> 16:
				print('Port too long')
				return 
			
			


			self.socket = protocol(self.address)
			self.socket.connection_callback(self.connect)
			threading.Thread(target=self.socket.listen, daemon=True).start()
			

			with open(LOG,'w') as log:
				print(*self.address,sep=SEP,file=log)							

			self.main.address.start.config(command=self.client,text='Connect')
			tkinter.Label(self.main.address, text='Listening:\n' + str(self.address)).pack()	
			print('Server address:\t',self.address)

			
		except ValueError:

			print('Invalid integer server port')	

	def connect (self, connection, address):		

		chat(self.main, connection, address, 'from')

	def client (self):		

		try:
			address = self.main.address.ip.get().strip(), int(self.main.address.port.get())					
			print('Connecting to',address)
			chat(self.main, self.socket.connect(address), address, 'to')

		except ValueError:
			print('Invalid integer client port')	

	def destroy (self):	
		print('Closing main window')
		
		global active
		active = False

		self.main.destroy()

		print(active)
		exit(0)

	def mainloop (self):	
		self.start()



class chat:

	def __init__ (self, m, c, a, l = ''):		
		

		self.main = tkinter.Toplevel(m)
		self.main.scrollable = self.main.screen = tkinter.Frame(self.main)
		self.main.scrollable.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
		self.main.window = tkinter.Canvas(self.main.scrollable)
		self.main.window.bar = tkinter.Scrollbar(self.main.scrollable, command=self.main.window.yview)
		self.main.window.bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		self.main.window.pack(fill=tkinter.BOTH, expand=True)
		self.main.window.config(yscrollcommand=self.main.window.bar.set)
		
		self.main.window.bind('<Configure>', self.update_window)
		

		self.main.screen = tkinter.Frame(self.main.window)
		self.main.screen.pack(fill=tkinter.BOTH, expand=True)
		self.main.window.create_window((0, 0), window=self.main.screen, anchor=tkinter.NW)
		
		self.main.chat = tkinter.Frame(self.main.screen)
		self.main.chat.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
		
		self.main.msg = tkinter.Frame(self.main)
		self.main.msg.pack(fill=tkinter.X)

		self.main.msg.send = tkinter.Button(self.main.msg, text='Run!', command=self.send)
		self.main.msg.send.pack(side=tkinter.LEFT, fill=tkinter.X, expand=True)
		self.main.msg.send.function = lambda e: self.main.msg.send.invoke()

		
		self.main.msg.delete = tkinter.Button(self.main.msg, text='Remove results', command=self.delete)
		self.main.msg.delete.pack(side=tkinter.RIGHT)

		self.main.protocol('WM_DELETE_WINDOW', self.destroy)

		

		self.n = TEST_ID
		
		
		
		
		self.connection = c
		self.connection.message_callback(self.mainloop)
		threading.Thread(target=self.connection.mainloop, daemon=True).start()
		self.address = a
		self.active = True
		self.last = {2:None}

		self.main.bind('<Return>', self.main.msg.send.function)
		self.main.title(protocol.__name__.upper() + ' ' + l + ' ' + str(a)) # mudando o título da conversa

		
		self.received = self.download = False
		self.upload = -2

		self.download_data = 0
		self.upload_data = -3

		self.errors = 0

		self.sent = self.download_time = self.download_size = 0
		
		self.test = -4

		
		print('Chatting with',self.address,'(Speed test)')

		
	def update_window (self, event = None):	

		self.main.window.update()
		self.main.window.configure(scrollregion=self.main.window.bbox(tkinter.ALL))

	def delete (self):

		self.main.chat.destroy()
		self.main.chat = tkinter.Frame(self.main.screen)
		self.main.chat.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)

		self.update_window()

		self.last = {2:None}


	def send (self):	
		
		
		
		self.n += 1
		

		# iniciar teste 
		threading.Thread(target=self.send_test, args=[TEST_TURNS], daemon=True).start()

		

	def send_test (self, remaining_tests, ask_data = True):
		
		self.test = remaining_tests
		self.main.msg.send.config(state=tkinter.DISABLED)
		self.main.bind('<Return>', print)
		
		
		begin = self.package(self.encode_in_bytes(self.n),b'\x7f\0',b'\x7f\0')

		d = self.received = False
		while self.active and not self.received: 
			time.sleep(0.5)
			print('Waiting confirmation\t',d)
			self.connection.sendall(begin) # envia pacotes de início 	
			d += 1
			time.sleep(1)

		print('Sending....')	
		
		ti = time.time()
		tf = ti + ((remaining_tests > 0) * TEST_TIME / 1000)
		c = 0
		ck = self.package()

		while time.time() <= tf:
			
			c += 1 	

			self.connection.sendall(ck)

		finish = self.package(self.encode_in_bytes(c), self.encode_in_bytes(remaining_tests), self.encode_in_bytes(TEST_TIME) + self.encode_in_bytes(SIZE) + (b'\x7f\0\x7f\0\x7f\0' if ask_data else (self.encode_in_bytes(self.download_data) + self.encode_in_bytes(self.errors) + self.encode_in_bytes(self.download))))
		print([remaining_tests], c, 'packages sent')	
		

		d = self.received = False
		while self.active and not self.received: 
			time.sleep(1)
			print('Waiting for response\t',d)
			self.connection.sendall(finish) # envia pacotes de finalização 	
			d += 1
			time.sleep(1.5)

		
			

		if c:
			self.sent = c

		if remaining_tests <= 1:
			
			self.main.msg.send.config(state=tkinter.ACTIVE)	
			self.main.bind('<Return>', self.main.msg.send.function)	

			if remaining_tests < 1:

				print('Closing\t',self.download,self.download_data)	
				
			self.test = -4
			
		print('Responded')	
			

				
	def package (self, number = b'\0', test_number = b'', r = b''):			

		 

		header = r + test_number + number + b'\0'

		

		return header + (TEST_TEXT * math.ceil(SIZE / len(TEST_TEXT))).encode()[:SIZE - len(header)] # MSG_TEXT



	def encode_in_bytes (self, n, end=b'\0'):	

		v = b = c = 0

		while n > 0:

			v += ((n % 128) + 128) << c
			n >>= 7
			c += 8
			b += 1
		
		if b:
			return v.to_bytes(b, 'big') + end

		
			
		return b'\x80' + end	
			
	def convert_size (self, v, k_div = 1024, k_if = 1000):

		s = k = 0
		if v < 0:
			s = True
			v = -v
		while v > k_if:
			v /= k_div			
			k += 1

		if type(v) == float and v.is_integer():	
			v = int(v)

		if s:
			v = -v	

		return v, k	
				
					

				 

				
						
					
							
			
	

	def mainloop (self, msg):	

		m = n = i = f = t = r = False
		v = []
				
		while len(msg) > f: 
			c = msg[f]
			
			if c:	
				m = (m << 7) + c - 128 
			else:	#\0	
				if i >= f:
					break # acaba com \0\0
				r = t	
				t = n

				n = m
				v.append(m)
				m = False #ord(msg[i:f].decode()) - 128
				
				i = f + 1
			f += 1		
			
		else:		
			# número do pacote, número do teste, índices inicial e final de leitura do texto, lista de valores
			print('ERROR\t',m,n,t,r,'\t',[i,f],v,'\t',self.download, self.errors) 
			self.errors += 1
			return 

		self.received = True	
	#	print((i,f),v,'\t',m,n,t,r)

		if t > 0: 
			if self.test < t and self.test >= 0:
				print('Repeated confirmation')
				return
			threading.Thread(target=self.send_test, args=(t - 1, False), daemon=True).start()
		elif r > 0 or r == -1:	
			
			if self.n < n and t < 0 and t >= -2:
				print(self.n, '<', n)
				self.n = n

			if t == -2: # recebimento da confirmação 
				return

			self.connection.sendall(self.package(self.encode_in_bytes(self.n), b'~\0', b'\x7f\0'))
			if t == -1:
				print('Beginning....')
				self.download = self.download_data = self.errors = False
				self.test = -4
				self.main.msg.send.config(state=tkinter.DISABLED)
				self.main.bind('<Return>', print)

				
				
				return 
				
			print('Ending\t',self.download,self.download_data)	
			
			
			
		else:		
			self.download += 1		 
			self.download_data += len(msg)
			return

		print('FINISH\t', n, t, r, v)
		
		self.upload = r
		self.upload_error = -1
		if len(v):
			self.download_time = v[0]
			if len(v) > 1:
				self.download_size = v[1]
				if len(v) > 2:
					self.upload_data = v[2]
					if len(v) > 3:
						self.upload_error = v[3]
						
					
				
			
			
		
			
		data_sent = self.download_size * n	
		data_size, data_scale = self.convert_size(data_sent)
		lost_size, lost_scale = self.convert_size(data_sent - self.download_data)
		download_size, download_scale = self.convert_size(self.download_data)
		download_speed, download_prefix = self.convert_size(self.download_data * 8000 / self.download_time) if self.download_time > 0 else (-1, 0)
		upload_speed, upload_prefix = self.convert_size(self.upload_data * 8000 / TEST_TIME) if TEST_TIME > 0 else (-1, 0)
		upload_size, upload_scale = self.convert_size(self.upload_data)

		# 
		p = f'\nDownload {numf(self.n)}.{numf(t)}:\n\tSent {numf(n)} packages ({numf(data_size)} {SCALE_PREFIX[data_scale] if data_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(data_scale))}B)\n\t{numf(n - self.download)} lost and {numf(self.errors)} errors ({numf(lost_size)} {SCALE_PREFIX[lost_scale] if lost_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(lost_scale))}B)\n\tReceived {numf(self.download)} packages ({numf(download_size)} {SCALE_PREFIX[download_scale] if download_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(download_scale))}B = {numf(100 * self.download_data / data_sent) if data_sent else "--"}%)\n\t{numf(1000 * self.download / self.download_time) if self.download_time > 0 else "--"} packages/s = {numf(download_speed)} {SCALE_PREFIX[download_prefix] if download_prefix < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(download_prefix))}b/s' if t > 0 else 'The end.'

			

		data_sent = self.sent * SIZE
		data_size, data_scale = self.convert_size(data_sent)
		lost_size, lost_scale = self.convert_size(data_sent - self.upload_data)
		# 
		q = f'\nUpload {numf(self.n)}.{numf(t + 1)}:\n\tSent {numf(self.sent)} packages ({numf(data_size)} {SCALE_PREFIX[data_scale] if data_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(data_scale))}B)\n\t{numf(self.sent - self.upload)} lost {("and " + numf(self.upload_error) + " errors") if (self.upload_error >= 0) else "packages"} ({numf(lost_size)} {SCALE_PREFIX[lost_scale] if lost_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(lost_scale))}B)\n\tReceived {numf(self.upload)} packages ({numf(upload_size)} {SCALE_PREFIX[upload_scale] if upload_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(upload_scale))}B = {numf(100 * self.upload_data / data_sent) if data_sent else "--"}%)\n\t{numf(1000 * self.upload / TEST_TIME) if TEST_TIME > 0 else "--"} packages/s = {numf(upload_speed)} {SCALE_PREFIX[upload_prefix] if upload_prefix < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(upload_prefix))}b/s' if r > 0 else 'Beginning'
		
		print(q,'\n',SIZE,'Bytes/package\n',TEST_TIME,'ms\n',p,'\n',self.download_size,'Bytes/package\n',self.download_time,'ms')

		paragraph = tkinter.Frame(self.main.chat)
		t = time.localtime()[:5]
		if t != self.last:
			if t[2] != self.last[2]:
				tkinter.Label(paragraph, text='%02d/%02d/%d' %t[2::-1]).pack()
			self.last = t
			tkinter.Label(paragraph, text='%02d:%02d' %t[3:]).pack()								

		ln = tkinter.Frame(paragraph)
		ln.pack(fill=tkinter.X)
		tkinter.Label(ln, text=q).pack(side=tkinter.RIGHT)	

		ln = tkinter.Frame(paragraph)
		ln.pack(fill=tkinter.X)
		tkinter.Label(ln, text=p).pack(side=tkinter.LEFT)	

		paragraph.pack(fill=tkinter.X) 
			

		self.main.window.yview_moveto(0)
		self.update_window()
		
				
						


					
							

			
	def destroy (self):
		print('Closing window')
		self.connection.close(self.address)
		self.active = False
		self.main.destroy()

print('.') 
# ponto final avisa o fim das definições

if __name__ == '__main__':		
	import os
	print(os.system('ipconfig'))
	k = ' '
	for v in os.sys.argv:
		if k == 'sep':
			SEP = v
		elif k == 'log':
			LOG = v
		elif k == 'time':	
			TEST_TIME = math.floor(float(v) * 1000)
		elif k == 'turns':	
			TEST_TURNS = int(v)
		elif k == 'text':	
			TEST_TEXT = v
		elif k == 'size':	
			SIZE = int(v)
		elif k == 'protocol':
			protocol = {'tcp': tcp, 'udp': udp}[v.lower()]
		elif k == 'test':	
			TEST_ID = int(v)
		else:	
			k = v.lower()#.replace('-','').replace('_','')
			continue

		print(k,'\t',v)		
		k = ''

		

	main().start()	



