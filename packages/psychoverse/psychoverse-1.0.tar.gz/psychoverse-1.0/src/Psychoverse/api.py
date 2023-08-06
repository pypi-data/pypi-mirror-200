import requests
from server import server
class Token(str):
  def __init__(self, token):
    self.token = token
  def __str__(self):
    return self.token

class Api:
  def __init__(self, username, app_name, passwd):
    self.app_url = "https://psychoapi.kotlintitus.repl.co/u_"+username+"/app/"+app_name+"?passwd="+passwd
    requests.get()
  def token(self):
    return Token(requests.get(self.app_url).text)


    
class App:
  def __init__(self, api:Api):
    self.path = f"https://psychoapi.kotlintitus.repl.co/t_{api.token().token}/"
  def environ_set(self, name, value):
    res=requests.get(self.path+f"environ/set?name={name}&value={value}")
  def environ_get(self, name):
    return requests.get(self.path+f"environ/get?name={name}").text
  
  
    
    
    
    
    




    
    