import socket
import threading
import traceback
import json
from typing import Union


class Network:
    header = 500
    format = 'utf-8'

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8420

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @property
    def address(self):
        return self.host, self.port

    @address.setter
    def address(self, new: tuple):
        self.host, self.port = new


class Server(Network):
    def __init__(self):
        super(Server, self).__init__()
        self.sock.bind(self.address)
        self.lock = threading.Lock()

    def processData(self, data: bytes, addr: tuple[str, int]) -> Union[bool, tuple, int, str, list, dict]:
        # override this function in the child class.
        # data - msg received from client
        # addr - (host, port)
        pass

    def _handleClient(self, data, addr):
        msg = self.processData(data, addr)
        try:
            if msg:
                jsonObject = json.dumps(msg)
                byteObject = jsonObject.encode(self.format)

                with self.lock:
                    self.sock.sendto(byteObject, addr)
            else:
                with self.lock:
                    msg = 'received' if data else 'empty'
                    jsonObject = json.dumps(msg)
                    byteObject = jsonObject.encode(self.format)
                    self.sock.sendto(byteObject, addr)
        except KeyboardInterrupt:
            print("Closing server...")
        except Exception:
            traceback.print_exc()

    def run(self):
        print("[SERVER STARTED] ", self.address)

        try:
            while True:
                data, addr = self.sock.recvfrom(self.header)

                thread = threading.Thread(target=self._handleClient, args=(data, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nClosing server...")
        except Exception:
            traceback.print_exc()

    def __del__(self):
        self.sock.close()
        print("[SERVER CLOSED]")


class Client(Network):
    def __init__(self):
        super(Client, self).__init__()

    def requestServer(self, msg: Union[bool, tuple, int, str, list, dict]):
        try:
            jsonObject = json.dumps(msg)
            byteObject = jsonObject.encode(self.format)
            self.sock.sendto(byteObject, self.address)

            data, addr = self.sock.recvfrom(self.header)
            msg = json.loads(data.decode(self.format))
            return msg
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        except Exception:
            traceback.print_exc()

    def __del__(self):
        self.sock.close()
        print("[CLIENT EXITED]")
