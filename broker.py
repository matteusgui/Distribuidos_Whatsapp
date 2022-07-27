import string
from time import sleep
import zmq

def input_comando():
    comando = input("Coloque a palavra 'END' se quiser encerrar o programa: ")
    return comando

ctx = zmq.Context()

# Abre a porta 1101 para pub de modo local
subscriber = ctx.socket(zmq.XSUB)
subscriber.connect("tcp://localhost:1101")
subscriber.setsockopt(zmq.SUBSCRIBE, b'')

# Abre a porta 1102 para conexão de modo local
publisher = ctx.socket(zmq.XPUB)
publisher.bind("tcp://localhost:1102")

# Enquanto o servidor estiver ativo recebe as mensagens em partes e as envia para quem estiver ouvindo ao tópico
while True:
    msg = subscriber.recv_multipart()
    publisher.send_multipart(msg)
    sleep(0.00001)
    # Problema de não finalizar as conexões iniciadas, necessidade de um comando que o faça corretamente, para reutilização das portas