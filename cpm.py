#!/usr/bin/python

import sys
import zmq
import os

import click
import webbrowser

from message import com


servername = "localhost"#"rscpm"
serverport = "5555"
connectionInfo = "tcp://"+servername+":"+serverport
guihost = 'http://'+servername+':8080/'

context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.setsockopt(zmq.LINGER, 0)
sock.connect(connectionInfo)

@click.group()
def cli() :
  """CPM CLI - Corpus & Process Manager Command Line Interface"""
  pass

@cli.command()
def reload() :
  """Refresh cpm modules defintion"""
  print com.sendMessage(sock,"reload")

@cli.group()
def module() :
  """Manage cpm modules"""
  pass

def modulesls(name):
  return com.sendMessage(sock,"module ls"+name,10)
  
def modulehelp(name):
  return com.sendMessage(sock,"module getdesc "+name,10)

def modulefunc(name):
  @cli.command(help=modulehelp(name))
  @click.argument('conf_file')
  def func(conf_file):
    print com.sendMessage(sock,"module run "+name+" "+conf_file)
  return func


class CPMModules(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        modules = modulesls(" --name")
        for filename in modules.split("\n"):
            if filename.strip() != "":
                rv.append(filename)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        return modulefunc(name)




@cli.command(cls=CPMModules)
def run():
  """Shorthand for "module run" command"""
  pass
  

@module.command()
@click.option('--name', default=False,is_flag=True,help="Only print modules' name")
def ls(name):
  """List all available modules"""
  optname = ""
  if name :
    optname = " --name"
  print modulesls(optname)



@module.command(cls=CPMModules)
def run():
  """Run a MODULE with configuration file CONF_FILE"""
  pass


@cli.group()
def process():
  """Manage cpm process"""
  pass

@process.command()
@click.option('--all','-a', default=False,is_flag=True,help="List all processes (including stopped/finished processes)")
@click.option('--recursive','-r', default=False,is_flag=True,help="List also children processes")
def ls(all,recursive):
  """List running processes"""
  optall = ""
  optrec = ""
  if all :
    optall = " -a"
  if recursive :
    optrec = " -r"
  print com.sendMessage(sock,"process ls"+optall+optrec)

@process.command()
@click.argument('pid')
def status(pid):
  """Print the status of a process and its children processes if any"""
  print com.sendMessage(sock,"process status "+pid)

@process.command()
@click.argument('pid')
@click.argument('outputname')
@click.option('--gui','-g',default=False,is_flag=True,help="View graphical result in a browser")
def view(pid,outputname,gui):
  """View the output OUTPUTNAME of a module run PID"""
  optgui = ""
  if gui :
    optgui = " --gui"
  res = com.sendMessage(sock,"process view "+pid+" "+outputname+optgui)
  if gui :
    webbrowser.open(guihost+url)
  else :
    print res

@process.command()
@click.argument('pid')
@click.option('--gui','-g',default=False,is_flag=True)
def log(pid,gui):
  """View the default error log of a module run PID"""
  res = com.sendMessage(sock,"process log "+pid)
  print res


if __name__ == '__main__':
  cli()
    





