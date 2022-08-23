
print(end='\n.') # o primeiro ponto avisa que o programa abriu e está carregando
import socket # Internet Socket API 

print(end='.') # o segundo ponto avisa a abertura da segunda dependência
import threading  
import tkinter 
import time

print(end='.') # o terceiro ponto avisa a definição das classes 
LOG = 'ip_port.log'
SEP = '\t'


class main:

	def __init__ (self):
		self.main = tkinter.Tk()
		self.active = True

		self.chats = {} # conversas iniciadas		

		self.main.title('TCP chat') # mudando o título da janela principal 

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


			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

				server.bind(self.address)	
				with open(LOG,'w') as log:
					print(*self.address,sep=SEP,file=log)
				
				while self.active:

					server.listen()
					connection, address = server.accept()
					print('Accepted',address)
					if not address in self.chats:

						

						self.chats[address] = chat(self.main, connection, address, 'from')						

						threading.Thread(target=self.chats[address].start).start()

				print('Servidor inativo')


		except ValueError:

			print('Insira um inteiro válido na porta')	

	def client (self):		

		try:
			address = self.main.address.ip.get().strip(), int(self.main.address.port.get())					

			if not address in self.chats:

					print('Connecting to',address)

					client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

					client.connect(address)

					self.chats[address] = chat(self.main, client, address, 'to')						

					threading.Thread(target=self.chats[address].start).start()

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
		self.sending = []
		
		self.connection = c
		self.address = a
		self.active = True
		self.last = {2:None}

		self.main.bind('<Return>', self.main.msg.send.function)
		self.main.title(l + ' ' + str(a)) # mudando o título da conversa

		

	def start (self):	
		print('Chatting with',self.address)
		self.mainloop()

	def send (self):	
	#	self.main.msg.send.config(state=tkinter.DISABLED)
		self.main.bind('<Return>', print)
		filename = self.main.msg.text.get().strip()
		if len(filename):
			name = filename.split('/')[-1].split('\\')[-1]
			
			with open(filename, 'rb') as file:				
				c = 0
				while True:
					c += 1
					body = file.read(500)
					if len(body):
						self.sending.append((c,name,(f'{c}/{name}\\').encode() + body))																	 
					else: 	
						self.sending.append((c,name,(f'{c}/|{name}\\').encode()))
						break
			self.connection.sendall((f'0/{name}\\').encode())
			
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


			

	def mainloop (self):	
		with self.connection:
			while self.active:
				msg = self.connection.recv(1024)#.decode().strip()
				

				f = ''
				i = b = False
				
				while True:
					c = msg[i]
					i += 1	
					if c == 124:	#|
						print('EOF')
						b = True
					elif c == 47:	#/	
						print('Not done yet')	
						n = int(f)
						f = ''
					elif c == 92:	#\
						break
					else:
						f += chr(c)

				if len(f) or len(self.sending):
					if len(self.sending):
						c,name,msg = self.sending.pop(0)
						print('Sending:\t',name,c)
						self.connection.sendall(msg)	
					else:
						self.connection.sendall(b'\\')	
				if not len(f):	
					continue
				

				print(f,n,i)		
				if not f in self.files:
					print('Starting',f)
					self.files[f] = {'size':None}
				self.files[f][n] = msg[i:]	

				
				if b:
					self.files[f]['size'] = n + 2
					print('Size:',self.files[f]['size'],len(self.files[f]))
				if len(self.files[f]) == self.files[f]['size']:
					print('Saving',f)
					with open(f, 'wb') as file:
						for c in range(len(self.files[f])):
							if c in self.files[f]:
								file.write(self.files[f][c])
								print(c, len(self.files[f][c]))
							else:
								print(c, len(self.files[f]))	

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

if __name__ == '__main__':		
	main().start()	



