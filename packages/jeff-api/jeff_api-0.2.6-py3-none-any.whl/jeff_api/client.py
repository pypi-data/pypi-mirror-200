import json, socket


class Client:
  def __init__(self, ip, port):
    self.ip = ip
    self.socket_port = port

  def _send(self, data):
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((self.ip, self.socket_port))
        sock.sendall(data)
    except ConnectionRefusedError:
      print('Jeff\'s socket is disabled.')

  def _accept(self, data, buffer_size):
    try:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((self.ip, self.socket_port))
        sock.sendall(data)
        data = sock.recv(buffer_size)
        while not len(data):
          data = sock.recv(buffer_size)
    except ConnectionRefusedError:
      print('Jeff\'s socket is disabled.')
    return data

  def _encode_json(j):
    return json.dumps(j).encode()

  def _decode_json(b):
    return json.loads(b.decode())

  def send_msg(self, msg):
    j = {"send": msg}
    self._send(Client._encode_json(j))

  def send_json(self, j):
    self._send(Client._encode_json(j))

  def send_as_user(self, msg):
    j = {"send_as_user": msg}
    self._send(Client._encode_json(j))

  def send_status(self, msg_id, msg):
    j = {"send_status": {"id": msg_id, "msg": msg}}
    self._send(Client._encode_json(j))

  def send_info(self, msg):
    j = {"send_info": msg}
    self._send(Client._encode_json(j))

  def send_error(self, msg):
    j = {"send_warning": msg}
    self._send(Client._encode_json(j))

  def store_cells(self, values_dict):
    j = {"store_in_memory": values_dict}
    self._send(Client._encode_json(j))

  def read_cell(self, key, buffer_size=8192):
    j = {"memory_cells": [key]}
    j = Client._decode_json(self._accept(Client._encode_json(j), buffer_size))
    if "memory_values" not in j: return None
    if key not in j["memory_values"]: return None
    return j["memory_values"][key]

  def read_cells(self, keys_arr, buffer_size=8192):
    j = {"memory_cells": keys_arr}
    j = Client._decode_json(self._accept(Client._encode_json(j), buffer_size))
    if "memory_values" not in j: return None
    return j["memory_values"]
