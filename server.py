import socket
import threading

from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True, convert=True)

HOST = "0.0.0.0"
PORT = 5000

clients = {}
lock = threading.Lock()

TITLE = Fore.MAGENTA
PRIMARY = Fore.CYAN
SUCCESS = Fore.GREEN
ERROR = Fore.RED
SYSTEM = Fore.WHITE


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def remove_client(client):
    with lock:
        if client not in clients:
            return

        pseudo = clients.pop(client)

    client.close()

    print(
        ERROR
        + f"[{timestamp()}] [-] {pseudo} disconnected "
        + f"({len(clients)} online)"
    )


def broadcast(message, sender=None):
    with lock:
        for client in list(clients):
            if client != sender:
                try:
                    client.sendall(message)
                except:
                    remove_client(client)


def handle_client(client, address):
    pseudo = "Unknown"

    print(
        PRIMARY
        + f"[{timestamp()}] [+] Connection from {address}"
    )

    try:
        while True:
            data = client.recv(4096)

            if not data:
                break

            message = data.decode(
                "utf-8",
                errors="replace"
            )

            if message.startswith("__JOIN__:"):
                pseudo = message.split(":", 1)[1]

                with lock:
                    clients[client] = pseudo

                print(
                    SUCCESS
                    + f"[{timestamp()}] [+] {pseudo} joined "
                    + f"({len(clients)} online)"
                )

                broadcast(
                    f"[+] {pseudo} joined the chat.".encode(),
                    client
                )

                continue

            print(
                SYSTEM
                + f"[{timestamp()}] [MSG] {pseudo}: {message}"
            )

            broadcast(
                message.encode(),
                client
            )

    except Exception as e:
        print(
            ERROR
            + f"[{timestamp()}] [!] {address}: {e}"
        )

    finally:
        if pseudo != "Unknown":
            broadcast(
                f"[-] {pseudo} left the chat.".encode(),
                client
            )

        remove_client(client)


def start():
    print(TITLE + Style.BRIGHT + r"""
 █████╗ ██████╗ ███████╗██╗   ██╗
██╔══██╗██╔══██╗██╔════╝██║   ██║
███████║██║  ██║█████╗  ██║   ██║
██╔══██║██║  ██║██╔══╝  ╚██╗ ██╔╝
██║  ██║██████╔╝███████╗ ╚████╔╝
╚═╝  ╚═╝╚═════╝ ╚══════╝  ╚═══╝

          A D E V   C H A T
             SERVER
""")

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, PORT)
    )

    server.listen()

    print(
        PRIMARY
        + "════════════════════════════════════"
    )
    print(
        SYSTEM
        + " Host : "
        + PRIMARY
        + HOST
    )
    print(
        SYSTEM
        + " Port : "
        + PRIMARY
        + str(PORT)
    )
    print(
        PRIMARY
        + "════════════════════════════════════"
    )

    print(
        SUCCESS
        + f"[{timestamp()}] [+] Server started"
    )

    while True:
        client, address = server.accept()

        threading.Thread(
            target=handle_client,
            args=(client, address),
            daemon=True
        ).start()


if __name__ == "__main__":
    start()