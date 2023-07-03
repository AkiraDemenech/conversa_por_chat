
print(end='\n.') # o primeiro ponto avisa que o programa abriu e está carregando

import socket # Internet Socket API 

print(end='.') # o segundo ponto avisa a abertura da segunda dependência
import threading   
import time
import math




print(end='.') # o terceiro ponto avisa a definição das classes 

SCALE_PREFIX = '', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'


numf = lambda x: ('%.3f' %x) if type(x) == float and not x.is_integer() else str(x)
active = chat_autoincrement = True


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

def read_address (callback = print):
	a = None
	while True:
		try:
			a = input('IP:\t').strip(), int(input('Porta:\t'))	
		except ValueError:	
			print('Insira um inteiro válido na porta')
			continue
			

		if a[1] <= 1023:
			print('Não insira uma porta privilegiada')
			continue

		if a[1] > 65535:
			print('Insira uma porta de até 2 bytes')
			continue 

		try:		
			return callback(a)
		except Exception as ex:
			print('Repita a operação, houve uma falha:\n',ex)

#MSG_TEXT = (TEST_TEXT * math.ceil(SIZE / len(TEST_TEXT))).encode()

class main:

	def __init__ (self):		
		print('Speed test', protocol.__name__.upper())

	def start (self):					

		print('\nEsta janela:')  	

		read_address(self.server)

		print('\nInsira o outro dispositivo:')

		try:
			while True:
				read_address(self.client)
		except KeyboardInterrupt:	
			input()		
		

	def server (self, address):					 

		self.socket = protocol(address)
		self.socket.connection_callback(self.connect)
		self.address = address
		threading.Thread(target=self.socket.listen, daemon=True).start()			

	def connect (self, connection, address):		

		chat(connection, address, 'de')

	def client (self, address):		

		print('Conectando a',address)
		conn = self.socket.connect(address)
		time.sleep(0.1)
		c = chat(conn, address, 'para')			
		time.sleep(1)
		print('\n\nIniciando envio:')
		c.send()

	def destroy (self):					
		global active
		active = False		
		print(active)
		exit(0)

	def mainloop (self):	
		self.start()



class chat:

	def __init__ (self, c, a, l = ''):		
		global chat_autoincrement
		chat_autoincrement += 1
		self.id = {chat_autoincrement}
		
		print('Chat',self.id)																
		
		self.n = TEST_ID
		
		self.connection = c
		self.connection.message_callback(self.mainloop)
		threading.Thread(target=self.connection.mainloop, daemon=True).start()
		self.address = a
		self.active = True
		self.last = {2:None}
		
		print(protocol.__name__.upper(),l,a) # mudando o título da conversa

		
		self.received = self.download = False
		self.upload = -2

		self.download_data = 0
		self.upload_data = -3

		self.errors = 0

		self.sent = self.download_time = self.download_size = 0
		self.test = -4

		self.turns = TEST_TURNS

		
		print(self.id,'testando a velocidade da conexão com',self.address,'\n')	

	def delete (self):		
		self.last = {2:None}


	def send (self):	
		self.n += 1
		self.turns = TEST_TURNS

		# iniciar teste 
		print(self.turns)
		self.send_test(self.turns)

		

	def send_test (self, remaining_tests, ask_data = True):
		
		print(self.test)
		self.test = remaining_tests				
		begin = self.package(self.encode_in_bytes(self.n), b'\x7f\0', self.encode_in_bytes(self.turns) + b'\x7f\0')

		d = self.received = False
		while self.active and not self.received: 
			time.sleep(0.5)
			print(self.id,'\t','Aguardando confirmação\t',d)
			self.connection.sendall(begin) # envia pacotes de início 	
			d += 1
			time.sleep(1)

		print(self.id,'\t','Enviando....')	
		
		ti = time.time()
		tf = ti + ((remaining_tests > 0) * TEST_TIME / 1000)
		c = 0
		ck = self.package()

		while time.time() <= tf:
			
			c += 1 	

			self.connection.sendall(ck)

		finish = self.package(self.encode_in_bytes(c), self.encode_in_bytes(remaining_tests), self.encode_in_bytes(TEST_TIME) + self.encode_in_bytes(SIZE) + (b'\x7f\0\x7f\0\x7f\0' if ask_data else (self.encode_in_bytes(self.download_data) + self.encode_in_bytes(self.errors) + self.encode_in_bytes(self.download))))
		print(self.id,'\t',[remaining_tests], c, 'pacotes enviados')	
		

		d = self.received = False
		while self.active and not self.received: 
			time.sleep(1)
			print(self.id,'\t','Aguardando resposta\t',d)
			self.connection.sendall(finish) # envia pacotes de finalização 	
			d += 1
			time.sleep(1.5)

		if c:
			self.sent = c

		if remaining_tests <= 1:							

			if remaining_tests < 1:

				print(self.id,'\t','Fechando\t',self.download,self.download_data)	
				
			self.test = -4
			
		print(self.id,'\t','Respondido')	
				
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
				

	def mainloop (self, msg, start = print):	

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
			print(self.id,'\n','ERRO\t',m,n,t,r,'\t',[i,f],v,'\t',self.download, self.errors) 
			self.errors += 1
			return 

			
	#	print((i,f),v,'\t',m,n,t,r)

		if t > 0: 
			if self.test < t and self.test >= 0:
				print(self.id,'\t','Confirmação repetida')
				self.received = True
				return
			start = threading.Thread(target=self.send_test, args=(t - 1, False), daemon=True).start
		elif r > 0 or r == -1:	
			
			if self.n < n and t < 0 and t >= -2:
				print(self.id,'\t',self.n, '<', n)
				self.n = n

			if t == -2: # recebimento da confirmação 
				self.received = True
				return

			start = lambda pack=self.package(self.encode_in_bytes(self.n), b'~\0', b'\x7f\0'): self.connection.sendall(pack) 
			if t == -1:
				start() # confirmação 
				print(self.id,'\t','Iniciando....', v[:1])
				self.download = self.download_data = self.errors = False
				self.test = -4
				self.turns = v[0]				
				self.received = True
				return 
				
			print(self.id,'\t','Terminando\t',self.download,self.download_data)	
			
		else:		
			self.received = True
			self.download += 1		 
			self.download_data += len(msg)
			return

		print(self.id,'\t','FIM\t', n, t, r, v)
		
		if (t > 0 and len(v) <= 1) or (r > 0 and len(v) <= 3):
			print(self.id,'\t','DADOS INCOMPLETOS!\n')
			return 
		
		
		self.upload = r
		self.download_time = v[0] if len(v) else 0
		self.download_size = v[1] if len(v) > 1 else -1
		self.upload_data = v[2] if len(v) > 2 else -1
		self.upload_error = v[3] if len(v) > 3 else -1

		if (t > 0 and (self.download_time <= 0 or self.download_size < 0)) or (r > 0 and (self.upload_data < 0 or self.upload_error < 0)):
			print(self.id,'\t','DADOS CORROMPIDOS!!\n')
			return

		print(self.id,'\t','Ok')	
		self.received = True			
									
		data_sent = self.download_size * n	
		data_size, data_scale = self.convert_size(data_sent)
		lost_size, lost_scale = self.convert_size(data_sent - self.download_data)
		download_size, download_scale = self.convert_size(self.download_data)
		download_speed, download_prefix = self.convert_size(self.download_data * 8000 / self.download_time) if self.download_time > 0 else (-1, 0)
		upload_speed, upload_prefix = self.convert_size(self.upload_data * 8000 / TEST_TIME) if TEST_TIME > 0 else (-1, 0)
		upload_size, upload_scale = self.convert_size(self.upload_data)
		# 
		p = f'\nDownload {numf(self.n)}.{numf(self.turns - t + 1)}: \n\tEnviados {numf(n)} pacotes ({numf(data_size)} {SCALE_PREFIX[data_scale] if data_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(data_scale))}B) \n\t{numf(1000 * n / self.download_time) if self.download_time > 0 else "--"} pacotes/s \n\t{numf(n - self.download)} perdidos e {numf(self.errors)} erros ({numf(lost_size)} {SCALE_PREFIX[lost_scale] if lost_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(lost_scale))}B) \n\tRecebidos {numf(self.download)} pacotes ({numf(download_size)} {SCALE_PREFIX[download_scale] if download_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(download_scale))}B = {numf(100 * self.download_data / data_sent) if data_sent else "--"}%)  \n\t{numf(1000 * self.download / self.download_time) if self.download_time > 0 else "--"} pacotes/s = {numf(download_speed)} {SCALE_PREFIX[download_prefix] if download_prefix < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(download_prefix))}b/s' if t > 0 else 'Fim.'

		data_sent = self.sent * SIZE
		data_size, data_scale = self.convert_size(data_sent)
		lost_size, lost_scale = self.convert_size(data_sent - self.upload_data)
		# 
		q = f'\nUpload {numf(self.n)}.{numf(self.turns - t)}: \n\tEnviados {numf(self.sent)} pacotes ({numf(data_size)} {SCALE_PREFIX[data_scale] if data_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(data_scale))}B) \n\t{numf(1000 * self.sent / TEST_TIME) if TEST_TIME > 0 else "--"} pacotes/s  \n\t{numf(self.sent - self.upload)} perdidos {("e " + numf(self.upload_error) + " erros") if (self.upload_error >= 0) else "pacotes"} ({numf(lost_size)} {SCALE_PREFIX[lost_scale] if lost_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(lost_scale))}B) \n\tRecebidos {numf(self.upload)} pacotes ({numf(upload_size)} {SCALE_PREFIX[upload_scale] if upload_scale < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(upload_scale))}B = {numf(100 * self.upload_data / data_sent) if data_sent else "--"}%)  \n\t{numf(1000 * self.upload / TEST_TIME) if TEST_TIME > 0 else "--"} pacotes/s = {numf(upload_speed)} {SCALE_PREFIX[upload_prefix] if upload_prefix < len(SCALE_PREFIX) else (SCALE_PREFIX[1] + "^" + str(upload_prefix))}b/s' if r > 0 else 'Início'
		
		start() # inicia a nova chamada, se houver 
		

		
		t = time.localtime()[:5]
		if t != self.last:
			if t[2] != self.last[2]:
				print(end='\t%02d/%02d/%d' %t[2::-1])
			self.last = t
			print('\t%02d:%02d' %t[3:])								

		print('\n',self.id,'\n\n',q,'\n\n',SIZE,'Bytes/pacote\n\n',TEST_TIME,'ms\n\n',p,'\n\n',self.download_size,'Bytes/pacote\n\n',self.download_time,'ms\n\n')			
					
	def destroy (self):
		print('Fechando janela\t',self.id)
		self.connection.close(self.address)
		self.active = False
		

print('.') 
# ponto final avisa o fim das definições

if __name__ == '__main__':		
	import os

	if os.system('ip address show'):
		if os.system('ifconfig'):
			if os.system('ipconfig'):	
				print('IP command unknown')
	
	k = ' '
	n = True
	for v in os.sys.argv:
		if k == 'time':	
			TEST_TIME = math.floor(float(v) * 1000)
		elif k == 'turns':	
			TEST_TURNS = int(v)
		elif k == 'text':	
			TEST_TEXT = v
		elif k == 'size':	
			SIZE = int(v)
		elif k == 'test':	
			TEST_ID = int(v)
		else:	
			
			k = v.lower()#.replace('-','').replace('_','')

			if k == 'udp':	
				protocol = udp
			elif k == 'tcp':
				protocol = tcp
			else:	
				continue

		print(k,'\t',v)		
		k = ''

		
	m = main()
	

	m.start()	
	input('Pressione enter para sair')