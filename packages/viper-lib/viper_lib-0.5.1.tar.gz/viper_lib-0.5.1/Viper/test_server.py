from asyncio import run
from Viper.async_utils import sock_poll_recv, sock_poll_send
import socket
from time import sleep

host = "localhost"

sock = socket.create_server((host, 0))
print("Listening on", sock.getsockname())

sock, add = sock.accept()
print("Connected to", sock.getpeername())

input("Press enter to start receiving data.")
print("Press Ctrl+C to stop receiving data.")

async def main():
    try:
        while True:
            if await sock_poll_recv(sock, 1):
                print("Receiving...", end="")
                sock.recv(2 ** 30)
                print("Done")
            else:
                print("Is the connection down?")
            print("Sleeping")
            sleep(10)
            print("Resuming")
    except KeyboardInterrupt:
        print("Exiting.")


run(main())