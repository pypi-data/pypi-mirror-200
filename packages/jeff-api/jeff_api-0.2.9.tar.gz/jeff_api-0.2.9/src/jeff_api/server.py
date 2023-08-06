import json, signal, socket


class Server:
  def __init__(self, host, port):
    self.host = host if host is not None else "0.0.0.0"
    self.port = port
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server_socket.bind((self.host, self.port))
    self.server_socket.listen()

    def exit_gracefully(*args):
      self.server_socket.close()

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

  def _waits_for(self, buffer_size=8192):
    try:
      (socket, address) = self.server_socket.accept()
      data = socket.recv(buffer_size)
      socket.close()
      return data
    except ConnectionRefusedError:
      print("Connection refused.")
      return b"{}"
    except json.decoder.JSONDecodeError:
      print('JSON decode error.')
      return b"{}"

  def _encode_json(j):
    return json.dumps(j).encode()

  def _decode_json(b):
    return json.loads(b.decode())

  def listen(self):
    return Server._decode_json(self._waits_for())
