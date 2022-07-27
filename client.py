import string
import zmq
import asyncio
import inspect

class client:
	def __init__(self, nome: string):
		self.nome = nome
	
	def create_topic():
		print("create_topic executou")
	
	def create_message():
		print("create_message executou")
	def subscribe():
		print("subscribe executou")
	def unsubscribe():
		print("unsubscribe executou")
	def exit():
		print("exit executou")

	def validar_comando(self, comando: string):
		comando = comando.strip()
		start = 0
		end = 0
		array = ['','','']
		vago = False
		j = 0
		for i in range(len(comando)):
			if vago:
				if comando[i] != ' ':
					vago = False
					start = i
					if(j == 2):
						array[2] == comando[i:len(comando)]
						break
			else:
				if comando[i] == ' ':
					array[j] = comando[start:i] 
					j+=1
					vago = True
						
				
		array[j] = comando[start:len(comando)]



		for i in range(len(array)):
			array[i] = array[i].strip()
		
		

		print(array)

		tsl = 5 #topic_size_limit
		msl = 7 #message_size_limit
		valido = True

		command_dic = {
			"create_topic": 2,
			"create_message": 3,
			"subscribe": 2,
			"unsubscribe": 2,
			"exit": 1
		}
		
		arg_size = command_dic.get(array[0])
		if(arg_size == None):
			print("Comando nao encontrado")
			valido = False

		elif(len(array) != command_dic[array[0]]):
			print(f'Comando "{array[0]}" espera {command_dic[array[0]]} argumento(s)')
			valido = False
		elif(array[0] != "exit"):
			if(len(array[1]) > tsl):
				print(f'Topico "{array[1]}" possui tamanho de {len(array[1])} caracteres. Limite é {tsl}')
				valido = False
			if(array[0] == "create_message"):
				if(len(array[2]) > msl):
					print(f'Mensagem "{array[2]}" possui tamanho de {len(array[2])} caracteres. Limite é {msl}')
					valido = False

		if(valido):
			print("Comando valido")
		return array if valido else None
		

		


a = client("salve")
exit = False
while(exit == False):
	batata = input()
	print(a.validar_comando(batata))


