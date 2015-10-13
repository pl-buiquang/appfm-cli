import zmq
import sys


def sendMessage(sock,message):
  sock.send_string(message)
  print sock.recv()


