
print(end='\n.') # o primeiro ponto avisa que o programa abriu e está carregando
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

BURST = 4
TIMEOUT = 25
SIZE = 1500

tcp = lambda: socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp = lambda: socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

protocol = tcp

class main:

	def __init__ (self):
		self.main = tkinter.Tk()
		self.active = True

				

		self.main.title('TCP chat (File transfer)') # mudando o título da janela principal 

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

		self.main.address.start = tkinter.Button(self.main.address.container, text='Start', command=lambda: threading.Thread(target=self.server).start())
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
			
			self.main.address.start.config(command=self.client,text='Connect')
			tkinter.Label(self.main.address, text='Listening:\n' + str(self.address)).pack()	
			print('Server address:\t',self.address)


			with protocol() as server:

				server.bind(self.address)	
				with open(LOG,'w') as log:
					print(*self.address,sep=SEP,file=log)
				
				while self.active:

					server.listen()
					connection, address = server.accept()
					print('Accepted',address)
					

						

						 						

					threading.Thread(target=chat(self.main, connection, address, 'from').start).start()

				print('Servidor inativo')


		except ValueError:

			print('Insira um inteiro válido na porta')	

	def client (self):		

		try:
			address = self.main.address.ip.get().strip(), int(self.main.address.port.get())					

			

			print('Connecting to',address)

			client = protocol()

			client.connect(address)

					 						

			threading.Thread(target=chat(self.main, client, address, 'to').start).start()

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
		self.address = a
		self.active = True
		self.last = {2:None}

		self.main.bind('<Return>', self.main.msg.send.function)
		self.main.title(l + ' ' + str(a)) # mudando o título da conversa

		self.size = SIZE
		self.burst = BURST
		self.burst_ack_timeout = TIMEOUT #ms
		self.burst_ack = {}

		

	def start (self):	
		print('Chatting with',self.address,'(File transfer)')
		self.mainloop()

	def send (self):	
	#	self.main.msg.send.config(state=tkinter.DISABLED)
		self.main.bind('<Return>', print)
		filename = self.main.msg.text.get().strip()
		if len(filename):
			name = filename.split('/')[-1].split('\\')[-1]
			queue = []
			with open(filename, 'rb') as file:				
				c = 0
				while True:
					c += 1
					head = (f'{hex(c)[2:]}/{name}\\').encode()

					if len(head) < self.size:
						body = file.read(self.size - len(head))
					else:	
						body = file.read(self.size)
						print('File too large:\t',c,name)															
						return
					
					# último pacote do arquivo
					if len(body) + len(head) < self.size:
						queue.append((c,name,('|'*(self.size-len(body)-len(head))).encode() + head + body))
						break
					queue.append((c, name, head + body))																	 
					 	
						

			while len(self.sending) > 0:		
				print('Waiting',len(self.sending))
				time.sleep(len(self.sending)/(1 + len(self.sending)))
				
			
			# primeiro pacote do arquivo
			pre = f'{hex(self.burst)[2:]}/{hex(self.size)[2:]}/{hex(len(queue))[2:]}|/'
			pos = '/' + name + '\\'

			queue.insert(0, (False, name, (pre + ('0' * (self.size - len(pre) - len(pos))) + pos).encode()))

			print(name,len(queue),self.size)
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
				time.sleep(1 / 100) 
				continue

			print('Burst:\t',len(self.sending),'left')

			for t in range(self.burst_ack_timeout):
				if c in self.burst_ack:
					print('Burst ACK (',len(self.burst_ack),'):\tpackage',self.burst_ack[c],'\t',t,'ms')
					break 
				time.sleep(1 / 1000)
			else:
				print('Burst ACK timeout')
				for name, c in burst:
					self.sending.insert(0,(c,name,self.sending_files[(name,c)]))
				lost.extend(burst)
					
				
				self.burst_ack_timeout <<= 1 # dobramos o timeout, caso seja lentidão na rede	
			burst.clear()	

		tf = time.time()		

		print(locale.format_string('%.6f', tf - ti, grouping=True),'s\t', (locale.format_string('%.6f', (len(lost) + c + 1) * self.size / ((tf - ti) * (2**17)), grouping=True) + ' total Mb/s'))	
		print(locale.format_string('%d', len(lost) + c + 1, grouping=True), 'sent (' + locale.format_string('%d', c + 1, grouping=True), 'unique packages),')
		print(locale.format_string('%d', len(lost), grouping=True), 'lost (' + locale.format_string('%d', len(set(lost)), grouping=True), 'unique packages):')
		
		for f, l in lost:
			print(f, '\t', l)

			


			
	def send_burst_ack (self, file, package):		

		self.connection.sendall(('/-a/' + hex(len(self.files[file]['data']) - 1)[2:] + '/' + hex(package)[2:] + '/\\').zfill(self.size).encode())

	def mainloop (self):	
		with self.connection:
			while self.active:
				msg = self.connection.recv(self.size)#.decode().strip()
				

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
					continue

				
				ti = time.time()
				

						
				if not f in self.files:

					
					
					print('Starting',f,'\t','%d-%d-%d_%d-%d-%d' %time.localtime(ti)[:6])
					self.files[f] = {'size':None,
									'last':False,
									'start':ti,'end':ti,
									'repeated': [],
									'done':False,
									'data':{}}
				

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
						self.size = k
						if j:
							self.burst = j
							print('Burst size:',j)
						print('Package size:',self.size)
						
				if len(self.files[f]['data']) == self.files[f]['size']:
					self.send_burst_ack(f, n)
					print('Sending final burst ACK')
					dt = ti - self.files[f]['start']
					sz = self.files[f]['size'] * self.size
					print('Saving',f,'\t','%d-%d-%d_%d-%d-%d' %time.localtime(ti)[:6],'\t',locale.format_string('%.6f', dt, grouping=True),'s\n', locale.format_string('%d', sz, grouping=True), 'bytes (' + locale.format_string('%.3f', sz / (1024**2), grouping=True),'MB =',locale.format_string('%.3f', sz / (1024 * 128), grouping=True),'Mb)\t', (locale.format_string('%.6f', sz / (1024 * 128 * dt), grouping=True) + ' successful Mb/s') if dt else '')
					repeated = len(self.files[f]['repeated'])
				#	useful = self.files[f]['size']
				#	total = 
					print(locale.format_string('%d', repeated + self.files[f]['size'], grouping=True), 'packages received:')
					
					print(locale.format_string('%d', self.files[f]['size'], grouping=True), 'unique packages,')

					
					print(locale.format_string('%d', repeated, grouping=True), 'repeated packages:')
					for n, l in self.files[f]['repeated']: 
						print('\t', n, '\t', l)

					if self.files[f]['done']:	
						print('File already saved.')
						continue

				#	repeated = list(self.files[f]['repeated'])
				#	repeated.sort()

				#	print(locale.format_string('%d', , grouping=True), 'lost packages.')
					self.files[f]['end'] = ti
					
					with open(f, 'wb') as file:
						k = list(self.files[f]['data'])
						k.sort()
						for c in k:
							file.write(self.files[f]['data'][c])
							
					print(f,'saved.\n\r')	
					self.files[f]['done'] = True
				#	self.files.pop(f)	

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



