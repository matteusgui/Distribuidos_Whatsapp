import zmq
import zmq.asyncio
import asyncio

def main():
    ctx = zmq.Context()

    pub = ctx.socket(zmq.PUB)
    pub.connect("tcp://localhost:5556")
    msg = "MACA mensagem"
    while True:
        pub.send_string(msg)
        print(msg)

if __name__ == "__main__":
    main()