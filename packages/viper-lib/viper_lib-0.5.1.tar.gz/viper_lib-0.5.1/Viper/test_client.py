from random import randbytes
from Viper.async_utils import sock_poll_recv, sock_poll_send
import socket
from asyncio import run
from time import sleep


host = "localhost"

if not host:
    host = input("Enter the server's IP address > ")
port = int(input("Enter the server's port > "))

sock = socket.create_connection((host, port))
print("Connected to remote host as", sock.getsockname())

packet = randbytes(2 ** 20) * 2 ** 12
input("Press Enter to start sending data.")
print("Press Ctrl+C to stop sending data.")

# sock.setblocking(False)

async def main():
    try:
        while True:
            if not await sock_poll_send(sock, 0):
                print("I have to slow down!")
                await sock_poll_send(sock, float("inf"))
            try:
                print("Sending...", end="")
                n = sock.send(packet)
                print("Done")
            except BlockingIOError:
                n = 0
                print("Done with an exception")
            if n < len(packet):
                print("I could not send everything.")
    except KeyboardInterrupt:
        print("Exiting.")


run(main())