#!/usr/bin/python

'''
Corpus Process Manager CLI

Usage:
  cpm modules ls [-a]
  cpm modules run <module_name> <conf_file>

  cpm process ls
  cpm process <pid> (start | stop | restart | status) 
  cpm process 

Options:
  -a -all   Print all modules

'''

import sys
import zmq

import click


from message import com


servername = "localhost"#"rscpm"
serverport = "5555"
connectionInfo = "tcp://"+servername+":"+serverport

context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.connect(connectionInfo)

@click.group()
def cli() :
  pass

@cli.group()
def module() :
  pass

@module.command()
def ls():
  com.sendMessage(sock,"module ls")

@module.command()
@click.argument('module')
@click.argument('conf_file')
def run(module,conf_file):
  com.sendMessage(sock,"module run "+module+" "+conf_file)


@cli.command()
def test():
  import uilib
  print "yo"

if __name__ == '__main__':
    cli()





