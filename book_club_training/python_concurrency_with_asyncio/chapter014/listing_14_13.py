import socket
from listing_14_11 import CustomTask
from listing_14_12 import EventLoop


async def read_from_client(conn, loop: EventLoop):
    print(f"Чтение данных от клиента {conn}")
    try:
        while data := await loop.sock_recv(conn):
            print(f"Получены данные {data} от клиента!")
    finally:
        loop.sock_close(conn)


async def listen_for_connections(sock, loop: EventLoop):
    while True:
        print("Ожидание подключения...")
        conn, addr = await loop.sock_accept(sock)
        CustomTask(read_from_client(conn, loop), loop)
        print(f"Новое подключение к сокету {sock}!")


async def main(loop: EventLoop):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8000))
    server_socket.listen()
    server_socket.setblocking(False)

    await listen_for_connections(server_socket, loop)


event_loop = EventLoop()
event_loop.run(main(event_loop))
