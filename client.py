import socket
import threading

from datetime import datetime

from colorama import init, Fore, Style
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

init(autoreset=True, convert=True)

SERVER_IP = "0.0.0.0"
PORT = 5000

PRIMARY = Fore.CYAN
ERROR = Fore.RED
WARNING = Fore.YELLOW

def timestamp():
    return datetime.now().strftime("%H:%M:%S")


print(PRIMARY + Style.BRIGHT + r"""
 █████╗ ██████╗ ███████╗██╗   ██╗
██╔══██╗██╔══██╗██╔════╝██║   ██║
███████║██║  ██║█████╗  ██║   ██║
██╔══██║██║  ██║██╔══╝  ╚██╗ ██╔╝
██║  ██║██████╔╝███████╗ ╚████╔╝
╚═╝  ╚═╝╚═════╝ ╚══════╝  ╚═══╝

        A D E V   C H A T
""")

print(PRIMARY + "════════════════════════════════════")
print(" Server :", SERVER_IP)
print(" Port   :", PORT)
print(PRIMARY + "════════════════════════════════════")
print()

pseudo = input("Username > ")

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

session = PromptSession()
stop = threading.Event()


def receive():
    while not stop.is_set():
        try:
            data = client.recv(4096)

            if not data:
                stop.set()
                break

            message = data.decode(
                "utf-8",
                errors="replace"
            )

            with patch_stdout():

                if message.startswith("[+]"):
                    print(
                        PRIMARY
                        + f"[{timestamp()}] "
                        + message
                    )
                    continue

                if message.startswith("[-]"):
                    print(
                        ERROR
                        + f"[{timestamp()}] "
                        + message
                    )
                    continue

                if message.startswith("[") and "] :" in message:
                    end = message.find("]")
                    username = message[1:end]
                    content = message[end + 4:]

                    if username == pseudo:
                        print(
                            f"[{timestamp()}] [ME] {content}"
                        )
                    else:
                        print(
                            f"[{timestamp()}] [{username}] {content}"
                        )

                else:
                    print(
                        f"[{timestamp()}] {message}"
                    )

        except Exception as e:
            print(
                ERROR
                + f"[{timestamp()}] [!] ERROR : {e}"
            )
            stop.set()


try:
    client.connect(
        (SERVER_IP, PORT)
    )

    print(
        PRIMARY
        + f"[{timestamp()}] [+] Connected successfully."
    )

    client.sendall(
        f"__JOIN__:{pseudo}".encode()
    )

    print(
        PRIMARY
        + f"[{timestamp()}] [+] Joined the chat."
    )

    threading.Thread(
        target=receive,
        daemon=True
    ).start()

except Exception as e:
    print(
        ERROR
        + f"[{timestamp()}] [!] Connection failed : {e}"
    )
    exit()


with patch_stdout():
    while not stop.is_set():

        try:
            message = session.prompt("> ")

            if not message.strip():
                continue

            if message.lower() == "/quit":
                print(
                    WARNING
                    + f"[{timestamp()}] [-] Disconnecting..."
                )
                stop.set()
                break

            client.sendall(
                f"[{pseudo}] : {message}".encode()
            )

        except (KeyboardInterrupt, EOFError):
            stop.set()
            break

        except Exception:
            print(
                ERROR
                + f"[{timestamp()}] [!] Connection lost."
            )
            break


client.close()

print(
    WARNING
    + f"[{timestamp()}] [-] Goodbye!"
)