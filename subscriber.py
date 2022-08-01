import string
import threading
import zmq
import zmq.asyncio
import asyncio
import inspect
import time
from aioconsole import ainput
import warnings

warnings.filterwarnings("ignore")

#async def create_topic():
#	print("create_topic executou")
#	return None

def create_message(args):

	"subscriber.send(TOPIC+ " " + MESSAGE "
	args[3].send_string(args[1] + " " + f"{args[4]} disse:" +args[2])

	return None
	
def subscribe(args):

	args[2].setsockopt_string(zmq.SUBSCRIBE, args[1])
	return None

def unsubscribe(args):
	args[2].setsockopt_string(zmq.UNSUBSCRIBE, args[1])
	return None

#Apenas retorna o estado "Exit" para que o console seja encerrado
def exit(args):
	return "Exit"


#Valida comando
#verifica se ele existe e possui os argumentos necessarios
#Verifica se os argumentos estao dentro das restricoes impostas
def validar_comando(comando: string):
	#----------------------------------------
	#Separa a string do comando em componentes menores
	#Contendo o comando em si e seus argumentos
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
	
	try:
		while(True):
			array.remove('')
	except:
		pass
	#---------------------------------------------------------------

	#Restricoes numero de argumentos, tamanhos do nomes do topic e mensagem 
	tsl = 5 #topic_size_limit
	msl = 7 #message_size_limit
	valido = True

	#Dicionario comando-numerodeargumentos
	command_dic = {
		#"create_topic": 2,
		"create_message": 3,
		"subscribe": 2,
		"unsubscribe": 2,
		"exit": 1
	}
	
	#Cadeia que valida os comandos
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

	#Printa uma mensagem validando o comando
	if(valido):
		print("Comando valido")
	#Se for valido retorna o comando separado em componentes menores
	#Se nao, retorna None
	return array if valido else None
		

def receptor(subscriber, control):
	while control.is_set():
		msg = subscriber.recv_string()
		if control.is_set():
			print(msg)
	return
	



def console(nome, publisher, subscriber, receptor, control):
	topic_unico = nome + bytes.fromhex('D2AF').decode('utf-8')
	topic_unico.upper()
	subscriber.setsockopt_string(zmq.SUBSCRIBE, topic_unico)
	
	#Dicionario comando-funcao
	str_fun_dic = {
		#"create_topic": (create_topic, publisher),
		"create_message": (create_message, publisher),
		"subscribe": (subscribe, subscriber),
		"unsubscribe": (unsubscribe, subscriber),
		"exit": (exit, [])
	}

	#Usuario insere comando, que eh validado, e se for permitido eh executadp
	#O comando Exit eh o unico que retorna um estado diferente de "Stay", saindo do loop
	estado = "Stay"
	while(estado != "Exit"):
		entrada = input()
		resposta = validar_comando(entrada)#Retorna None se o comando for invalido
		if resposta != None:
			func, modo = str_fun_dic[resposta[0]]
			estado = func(resposta + [modo] + [nome])
	
	control.clear()
	publisher.send_string(topic_unico + " " + "")
	return
	
def main():
	
	nome = ''
	while nome == '':
		nome = input("Insira seu nome: ")
		nome = nome.strip()
	

	p1 = "tcp://localhost:5556"
	p2 = "tcp://localhost:5559"
	ctx = zmq.Context()
	publisher = ctx.socket(zmq.PUB)
	subscriber = ctx.socket(zmq.SUB)
	publisher.connect(p1)
	subscriber.connect(p2)

	threads = []
	control = threading.Event()
	control.set()
	Recptor = threading.Thread(target=receptor, args=(subscriber,control))
	threads.append(Recptor)
	Recptor.start()
	Cnsole = threading.Thread(target=console, args=(nome, publisher, subscriber, Recptor,control))
	threads.append(Cnsole)
	Cnsole.start()
	for i in threads:
		i.join()


if __name__ == "__main__":
	main()
	#conectar ao servidor
	#definir modo
	#

	



 