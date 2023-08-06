import time
import requests
class General:
  def printt(string, speed, before=None):
    if speed is int:
      if speed >= 50:
        delay = 100 - speed
        delay = delay / 100
    elif speed == 'instant':
      delay = 0.1
    else:
      raise ValueError(f"maximum speed is 50, you put {speed}, which resulted in a delay of {(100 - speed) / 100}s")
    print(before, end='')
    for i in str(string):
      print(i, end="", flush = True)
      time.sleep(delay)
    print('')
  class Math:
    square = lambda x: x**2
    cube = lambda x: x**3
  Maths = Math
class Hastebin:
  def __init__(self, text):
    '''eg.
    data = Hastebin(input("Whats your name? "))
    print(f'Hello {data.text}!')
    debug = False
    if debug:
      print(data.data)
    print(data.url)'''
    self.text = str(text)
    self.data = requests.post("https://hastebin.com/documents", data=self.text)
    if self.data.text.startswith('<!DOCTYPE html>'):
      print('hastebin API is currently down')
    self.url = "https://hastebin.com/" + self.data.json()["key"]
class Fun:
  class Character:
    def __init__(self,name: str, script: list):
      self.chrname = name
      self.curline = 0
      self.lines = script
    def nextline(self):
      '''Go to next line'''
      self.curline += 1
    def prevline(self):
      '''Go to previous line'''
      self.curline -= 1
    def getline(self, sleep):
      '''Return current line'''
      return f'{self.lines[self.curline]}'
      time.sleep(sleep)
    def sendnext(self,sleep):
      '''Does both getline() and nextline()'''
      line = self.getline(sleep)
      self.nextline()
      return line
class Discord:
  def mentiontoid(mention: str):
    '''Used in commands that require user mentions'''
    numbers = '1234567890'
    for stri in mention:
      if stri not in numbers:
        mention = mention.replace(stri, '')
      else:
        continue
    return mention
class Bank:
  def __init__(self, max=999):
    self.max = max
    self.data = dict()
  def add_user(self, name: str):
    if name not in self.data:
      self.data[name] = 0
      return True
    else:
      return False
  def getbal(self, name: str):
    if name in self.data:
      return self.data[name]
    else:
      return
  def remove_user(self, name: str):
    if name in self.data:
      self.data.pop(name)
      return True
    else:
      return False
  def add_bal(self, bal:int, user:str):
    if user in self.data:
      if self.data[user] + bal < self.max + 1:
        self.data[user] + bal
        return True
      else:
        return False
    else:
      return False
  def give(self, give, recieve, amt: int):
    if give in self.data and recieve in self.data:
      if self.data[give] > amt + 1:
        if self.data[recieve] > self.max + 1:
          self.data[give] -= amt
          self.data[recieve] += amt
          return True
        else:
          return False
      else:
        return False
    else:
      return False
  def getdata(self):
    return self.data
class User:
  instances = []
  def __init__(self, name: str, password: str, bank: Bank, admin: bool):
    self.name = name
    self.passw = password
    self.isadm = admin
    bank.add_user(self.name)
    self.money = bank.data(self.namr)
    self.__class__.instances.append(self)
  @classmethod
  def login(cls, name: str, passw: str):
    for user in cls.instances:
      if user.name == name:
        nametrue = True
      else:
        nametrue = False
      if user.passw == passw:
        passtrue = True
      else:
        passtrue = False
      if nametrue and passtrue:
        loguser = user
        break
    if nametrue and passtrue:
      return loguser
    else:
      return False