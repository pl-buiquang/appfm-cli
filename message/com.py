import zmq
import sys
import socket
import os

class CPMCommand :

  def __init__(self,command,data="",user="",password=""):
    self.command = command
    self.data = data
    if user == "":
      user = os.environ['USER'] +'@'+ socket.gethostname()
    self.user = user
    self.password = password

  def toMessage(self):
    return "==USER=="+self.user+"==END_USER====PSWD=="+self.password+"==END_PSWD====CMD=="+self.command+"==END_CMD====DATA=="+self.data+"==END_DATA=="

  def send(sock,timeout=-1):
    return sendMessage(sock,self.toMessage(),timeout)


def sendMessage(sock,message,timeout=-1):
  sock.send_string(message)
  if timeout!=-1 :
    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)
    if poller.poll(timeout*1000): # 10s timeout in milliseconds
      msg = sock.recv()
    else:
      #raise IOError("Timeout processing cpm request")
      msg = "Timeout processing cpm request"
  else :
    msg = sock.recv()
  return msg

def sendCommand(sock,command,data="",timeout=-1):
  cpmcommand = CPMCommand(command,data)
  return sendMessage(sock,cpmcommand.toMessage(),timeout)


