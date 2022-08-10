import socket 


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((input('seu IP:').strip(), int(input('PORT:'))))
	s.listen()
	conn, addr = s.accept()
	with conn:
	
		print('Recebida conexão de', addr)
		while True:
			data = conn.recv(1024)
			if not data:
				print('Fim da comunicação.')
				break
			print('Mensagem recebida:',data.decode())	
			conn.sendall(input('Enviar resposta: ').encode())