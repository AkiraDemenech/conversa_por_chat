import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((input('SERVER IP:').strip(), int(input('PORT:'))))
	while True:
		s.sendall(input('Sua mensagem: ').encode())
		data = s.recv(1024)
		print('Resposta:',data.decode())