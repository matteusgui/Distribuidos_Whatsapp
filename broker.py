import zmq
import zmq.asyncio

ctx = zmq.Context.instance()
# Abre a porta 1101 para pub de modo local
subscriber = ctx.socket(zmq.XSUB)
subscriber.bind("tcp://*:5556")

# Abre a porta 1102 para conexão de modo local
publisher = ctx.socket(zmq.XPUB)
publisher.bind("tcp://*:5559")

# Enquanto o servidor estiver ativo recebe as mensagens em partes e as envia para quem estiver ouvindo ao tópico
print("proxy iniciando")
zmq.proxy(subscriber, publisher)

# Nunca chegamos nessa parte
subscriber.close()
publisher.close()
ctx.term()