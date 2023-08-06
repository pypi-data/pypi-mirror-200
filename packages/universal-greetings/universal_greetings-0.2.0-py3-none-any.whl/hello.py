import os

class Hello:
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  def __init__(self):
    self.myvar=os.getenv('MY_CUSTOM_VAR') or ''

  def sayHello(self):
    return 'Hello world!'
      

