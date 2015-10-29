import zmq
import sys


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


