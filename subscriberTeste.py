import zmq
import zmq.asyncio
import asyncio

def main():
    ctx = zmq.Context()

    sub = ctx.socket(zmq.SUB)
    sub.connect("tcp://localhost:5559")
    sub.setsockopt_string(zmq.SUBSCRIBE, "BANANA")
    sub.setsockopt_string(zmq.SUBSCRIBE, "MACA")

    print("Esperando receber a mensagem")
    i = 0
    while True:
        msg = sub.recv_string()
        print(msg)
        

if __name__ == "__main__":
    main()