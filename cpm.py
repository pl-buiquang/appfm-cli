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
import os

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

@cli.command()
def reload() :
  print com.sendMessage(sock,"reload")

@cli.group()
def module() :
  pass

def modulesls(name):
  return com.sendMessage(sock,"module ls"+name)

@module.command()
@click.option('--name', default=False,is_flag=True)
def ls(name):
  optname = ""
  if name :
    optname = " --name"
  print modulesls(optname)



@module.command()
@click.argument('module')
@click.argument('conf_file')
def run(module,conf_file):
  print com.sendMessage(sock,"module run "+module+" "+conf_file)


@cli.group()
def process():
  pass

@process.command()
@click.option('--all','-a', default=False,is_flag=True)
def ls(all):
  optall = ""
  if all :
    optall = " -a"
  print com.sendMessage(sock,"process ls"+optall)

@process.command()
@click.argument('pid')
def status(pid):
  print com.sendMessage(sock,"process status "+pid)



if __name__ == '__main__':
    cli()





