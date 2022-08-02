import string
import threading
import zmq
import zmq.asyncio
from aioconsole import ainput
import warnings

warnings.filterwarnings("ignore")

#Usuario cria uma mensagen MESSAGE no topico TOPIC com a conexao PUB
def create_message(args):
	#Utilizando termos da funcao console para melhor visualizacao
	#publisher.send(TOPIC+ " " + nome + "disse: " + MESSAGE)
	args[3].send_string(args[1] + " " + f"{args[4]} disse:" +args[2])

	return None

#Usuario se inscreve no topic TOPIC utilizando a conexao SUB
def subscribe(args):
	#Utilizando termos da funcao console para melhor visualizacao
	#subscriber.setsockopt_string(zmq.SUBSCRIBE, TOPIC)
	args[2].setsockopt_string(zmq.SUBSCRIBE, args[1])
	return None

#Usuario se desinscreve no topic TOPIC utilizando a conexao SUB
def unsubscribe(args):
	#Utilizando termos da funcao console para melhor visualizacao
	#subscriber.setsockopt_string(zmq.UNSUBSCRIBE, TOPIC)
	args[2].setsockopt_string(zmq.UNSUBSCRIBE, args[1])
	return None

#Usuario executado esta funcao para sair do loop, retornando a string "Exit"
def exit(args):
	return "Exit"


#Funcao escrite para validar comandos executados na funcao console utilizada pelo usuario
#verifica se ele existe e possui os argumentos necessarios
#Verifica se os argumentos estao dentro das restricoes impostas
def validar_comando(comando: string):
	#----------------------------------------
	#Quebra a string comando em partes menores, removendo
	#espaco entre seus argumentos, que serao validados
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
		"create_message": 3,
		"subscribe": 2,
		"unsubscribe": 2,
		"exit": 1
	}
	
	#Cadeia que valida os comandos.
	#Comandos foram estruturados seguindo a seguinte logica para uniformiza-los
	#Array[0]: nome do comando. Array[1]: nome do topico. Array[2]: mensagem
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


#A funcao receptor recebera mensagens do broker com a
#conexao SUB enquanto a variavel de controle for verdadeira
#Esta variavel de controle eh manipulada e atribuida falsa 
# pela funcao console quando o usuario encerrar a aplicacao
def receptor(subscriber, control):
	while control.is_set(): 
		msg = subscriber.recv_string() #Nota-se que esta funcao eh blocante, ou seja,
									   #permanecera em espera ate que alguma mensagen seja recebida do broker
		if control.is_set():
			print(msg)
	return
	



def console(nome, publisher, subscriber, receptor, control):
	#Para que a funcao receptor encerre seu ciclo de exeucao eh
	#necessario que a funcao blocante recv_string() receba uma ultima
	#mensagem, entao o usario eh inscrito em um topico em que o usuario
	#nao consiga acessar normalmente, e ao encerrar a aplicacao, o usuario
	#envia uma mensagem para este topico para sair a funcao blocante
	topic_unico = nome + bytes.fromhex('D2AF').decode('utf-8') #O nome to topico eh composto por um caracter especial
	topic_unico.upper()  
	subscriber.setsockopt_string(zmq.SUBSCRIBE, topic_unico)#Usuario eh inscrito neste topico "especial", inacessivel normalmente
	
	#Dicionario comando-funcao para simplificar fluxo de codigo
	str_fun_dic = {
		"create_message": (create_message, publisher), #Cria mensagem utilizando a conexao PUB
		"subscribe": (subscribe, subscriber), #Se inscreve no topico utilizando a conexao SUB
		"unsubscribe": (unsubscribe, subscriber), #Se desinscreve no topico utilizando a conexao SUB
		"exit": (exit, []) #Encerra aplicacao
	}

	#Usuario insere um comando, que eh validado, e se for permitido seus argumentos sao separados e eh executado
	#O comando Exit eh o unico que retorna um estado diferente de "Stay", saindo do loop
	estado = "Stay"
	while(estado != "Exit"):
		entrada = input() #Input do usuario
		resposta = validar_comando(entrada)#Retorna None se o comando for invalido, caso contrario, argumentos separados
		if resposta != None:
			func, modo = str_fun_dic[resposta[0]] #Recebe funcao do dicionario str_fun_dic fun e a conexao utilizada modo
			estado = func(resposta + [modo] + [nome])#A funcao eh executada com um array contando os argumentos, modo e nome do usuario
	
	control.clear()
	publisher.send_string(topic_unico + " " + "")
	return


#A funcao main estah dividida em 3 etapas:
def main():
	
	#1 - Receber o nome do usuario da aplicacao
	nome = ''
	while nome == '':
		nome = input("Insira seu nome: ")
		nome = nome.strip()
	
	#2 - Estabelecer conexaco com o broker como
	#PUB para enviar mensagens e SUB para receber mensagens
	p1 = "tcp://localhost:5556"
	p2 = "tcp://localhost:5559"
	ctx = zmq.Context()
	publisher = ctx.socket(zmq.PUB)
	subscriber = ctx.socket(zmq.SUB)
	publisher.connect(p1)
	subscriber.connect(p2)

	#3 - Iniciar duas threads para executar duas funcoes simulatenamente:
	threads = []
	control = threading.Event() #Variavel auxiliar de controle para finalizar a execucao da funcao receptor
	control.set()#Variavel de controle atribuida verdadeira

	#3.1 - A funcao receptor que recebera mensagens do broker utilizando
	#a conexao SUB e imprimir na tela
	Recptor = threading.Thread(target=receptor, args=(subscriber,control))
	threads.append(Recptor)
	Recptor.start()

	#3.2 A funcao console que recebera comandos do usuario, que podera:
	#Se inscrever e desinscrever de topicos com a conexao SUB
	#Enviar mensagens com a conexao PUB
	#Encerrar a aplicacao.
	Cnsole = threading.Thread(target=console, args=(nome, publisher, subscriber, Recptor,control))
	threads.append(Cnsole)
	Cnsole.start()

	for i in threads:
		i.join()

#Funcao inicial para chamar a funcao main
if __name__ == "__main__":
	main()
	

	



 