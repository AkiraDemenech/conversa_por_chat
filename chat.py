print(end='\n.') # o primeiro ponto avisa que o programa abriu e está carregando
import socket # Internet Socket API 

print(end='.') # o segundo ponto avisa a abertura da segunda dependência
import threading  
import tkinter 
import time

print('.') # o terceiro ponto avisa a definição das classes 

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

		tkinter.Label(self.main.address.container, text='IP:').pack(side=tkinter.LEFT)

		self.main.address.ip = tkinter.Entry(self.main.address.container)
		self.main.address.ip.pack(side=tkinter.LEFT)

		tkinter.Label(self.main.address.container, text='port:').pack(side=tkinter.LEFT)

		self.main.address.port = tkinter.Entry(self.main.address.container)
		self.main.address.port.pack(side=tkinter.LEFT)

		self.main.address.start = tkinter.Button(self.main.address.container, text='Start', command=lambda: threading.Thread(target=self.server).start())
		self.main.address.start.pack(side=tkinter.LEFT)
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


			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

				server.bind(self.address)	
				
				
				while self.active:

					server.listen()
					connection, address = server.accept()
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

		self.main.msg.text = tkinter.Entry(self.main.msg)
		self.main.msg.text.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

		
		self.connection = c
		self.address = a
		self.active = True

		self.main.title(l + ' ' + str(a)) # mudando o título da conversa

	def start (self):	
		self.mainloop()

	def send (self):	
		msg = self.main.msg.text.get().strip()
		if len(msg):
			self.connection.sendall(msg.encode())
			self.main.msg.text.delete(0,tkinter.END)
			paragraph = tkinter.Frame(self.main.chat)
			tkinter.Label(paragraph, text=msg).pack(side=tkinter.RIGHT)	
			paragraph.pack(fill=tkinter.X)

	def mainloop (self):	
		with self.connection:
			while self.active:
				paragraph = tkinter.Frame(self.main.chat)
				tkinter.Label(paragraph, text=self.connection.recv(1024).decode()).pack(side=tkinter.LEFT)	
				paragraph.pack(fill=tkinter.X)
			
	def destroy (self):
		self.active = False
		self.main.destroy()
if __name__ == '__main__':		
	main().start()	