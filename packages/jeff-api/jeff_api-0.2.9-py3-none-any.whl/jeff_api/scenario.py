import json


class ScenarioTerminatedException(Exception):
  "The scenario is ended by the user forcibly."
  pass


class ScenarioNotStartedException(Exception):
  "The scenario is ended by the user forcibly."
  pass


class Scenario:
  def __init__(self, cli, srv, name=None):
    self.cli = cli
    self.srv = srv
    self.init = False
    self.token = None
    self.nis = False
    if not name:
      self.name = f'Scenario at {self.srv.host}:{self.srv.port}'
    else:
      self.name = name

  def _encode_json(j):
    return json.dumps(j).encode()

  def _decode_json(b):
    return json.loads(b.decode())

  def _init_scenario(self, j):
    self.srv.server_socket.settimeout(5)
    ij = {"sready": True, "saddr": self.srv.host, "sport": self.srv.port, "sname": self.name}
    self.cli._send(Scenario._encode_json(ij))
    res = Scenario._decode_json(self.srv._waits_for())
    self.srv.server_socket.settimeout(None)
    if "stoken" in res:
      self.token = res["stoken"]
      self.init = True
      self._continue_scenario(j)
    elif "squeued" in res:
      while True:
        try: res = Scenario._decode_json(self.srv._waits_for())
        except UnicodeDecodeError: print('Unicode decode error.')
        if "stoken" not in res: raise ScenarioNotStartedException
        self.token = res["stoken"]
        self.init = True
        self._continue_scenario(j)
        break
    else:
      raise ScenarioNotStartedException

  def _continue_scenario(self, j):
    j |= {"stoken": self.token, "scontinue": True}
    self.cli._send(Scenario._encode_json(j))

  def _terminate_scenario(self, j):
    j |= {"stoken": self.token, "sfinish": True}
    self.token = None
    self.init = False
    self.nis = False
    self.cli._send(Scenario._encode_json(j))

  def _decide(self, j):
    if self.nis:
      self._terminate_scenario(j)
    elif self.init:
      self._continue_scenario(j)
    else:
      self._init_scenario(j)

  def send_msg(self, msg, last=False):
    if last:
      self.nis = True
    j = {"send": msg}
    self._decide(j)

  def send_as_user(self, msg, last=False):
    if last:
      self.nis = True
    j = {"send_as_user": msg}
    self._decide(j)

  def send_status(self, msg_id, msg, last=False):
    if last:
      self.nis = True
    j = {"send_status": {"id": msg_id, "msg": msg}}
    self._decide(j)

  def send_info(self, msg, last=False):
    if last:
      self.nis = True
    j = {"send_info": msg}
    self._decide(j)

  def send_error(self, msg, last=False):
    if last:
      self.nis = True
    j = {"send_warning": msg}
    self._decide(j)

  def store_cells(self, values_dict, last=False):
    if last:
      self.nis = True
    j = {"store_in_memory": values_dict}
    self._decide(j)

  def read_cells(self, keys_arr, buffer_size=8192):
    if not self.init or self.nis:
      return None
    j = {"memory_cells": keys_arr}
    j = Scenario._decode_json(self.cli._accept(Scenario._encode_json(j), buffer_size))
    if "memory_values" not in j:
      return None
    else:
      return j["memory_values"]

  def listen(self, buffer_size=8192):
    if not self.init or self.nis:
      raise ScenarioNotStartedException
    try:
      j = Scenario._decode_json(self.srv._waits_for(buffer_size))
    except UnicodeDecodeError:
      print('Unicode decode error.')
      return {}
    if "sfinish" in j:
      if j["sfinish"] is True:
        raise ScenarioTerminatedException
    return j

  def wait(self, buffer_size=8192):
    while True:
      msg = self.listen(buffer_size)
      if len(msg) == 0:
        continue
      if msg['author'] == 1:
        continue
      return msg['content']

  def terminate(self):
    self._terminate_scenario(dict())
