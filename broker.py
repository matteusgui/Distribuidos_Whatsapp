from matplotlib.pyplot import get
import zmq
import zmq.asyncio
import asyncio
from aioconsole import ainput, aprint
from requests import get

ip = get('https://api.ipify.org').content.decode('utf-8')
print('My public IP address is: {}'.format(ip))

ctx = zmq.Context.instance()
# Abre a porta 1101 para pub de modo local
subscriber = ctx.socket(zmq.XSUB)
subscriber.bind("tcp://*:7000")

# Abre a porta 1102 para conexão de modo local
publisher = ctx.socket(zmq.XPUB)
publisher.bind("tcp://*:7001")

# Enquanto o servidor estiver ativo recebe as mensagens em partes e as envia para quem estiver ouvindo ao tópico
print("proxy iniciando")
zmq.proxy(subscriber, publisher)

# Nunca chegamos nessa parte
subscriber.close()
publisher.close()
ctx.term()
# Problema de não finalizar as conexões iniciadas, necessidade de um comando que o faça corretamente, para reutilização das portas