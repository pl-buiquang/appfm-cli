#!/usr/bin/python

import sys
import zmq

servername = "localhost"#"rscpm"
serverport = "5555"
connectionInfo = "tcp://"+servername+":"+serverport

context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.connect(connectionInfo)
sock.send(' '.join(sys.argv[1:]))
print sock.recv()

