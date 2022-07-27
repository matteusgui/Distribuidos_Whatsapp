import zmq
import zmq.asyncio
import asyncio
from aioconsole import ainput

async def input_comando(task):
    valor = ""
    while valor != "END":
        valor = await ainput("Coloque a palavra 'END' se quiser encerrar o programa: ")
    task.cancel()
    return

async def zmqManager(subscriber: zmq.asyncio.Socket, publisher: zmq.asyncio.Socket):
    while True:
        msg = await subscriber.recv_multipart()
        await publisher.send_multipart(msg)

async def main():
    ctx = zmq.asyncio.Context()
    # Abre a porta 1101 para pub de modo local
    subscriber = ctx.socket(zmq.XSUB)
    subscriber.connect("tcp://localhost:1101")

    # Abre a porta 1102 para conexão de modo local
    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://*:1102")

    # Enquanto o servidor estiver ativo recebe as mensagens em partes e as envia para quem estiver ouvindo ao tópico
    tasks = [asyncio.create_task(zmqManager(subscriber, publisher))]
    tasks.append(asyncio.create_task(input_comando(tasks[0])))
    await asyncio.wait(tasks)
    return
    # Problema de não finalizar as conexões iniciadas, necessidade de um comando que o faça corretamente, para reutilização das portas

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()