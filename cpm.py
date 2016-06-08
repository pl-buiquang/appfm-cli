#!/usr/bin/python

import sys
import zmq
import os
import re

import click
import webbrowser

from message import com


def initConf() :
	defaultservername = "localhost"#"192.168.1.27"#"localhost"#"rscpm"
	defaultserverport = "5555"
	conffile = os.environ["HOME"]+"/.config/cpm.conf"
	conf = {
		"host":defaultservername,
		"port":defaultserverport
	}
	errormessage = "Using default value for connection : "+defaultservername+":"+defaultserverport
	if os.path.exists(conffile) :
		f = open(conffile,"r")
		try :
			for l in f:
				l = l.strip()
				if l.startswith("#") or l == "":
					continue
				else :
					variable = l.split(":")
  				conf[variable[0].strip()] = variable[1].strip()				
		except :
			conf = {
				"host":defaultservername,
				"port":defaultserverport
			}
			print "Unexpected error while reading configuration :", sys.exc_info()[0] 
	else :
		print "Couldn't find configuration file!"
		print errormessage
	return conf


conf=initConf()
connectionInfo = "tcp://"+conf["host"]+":"+conf["port"]



context = zmq.Context()

sock = context.socket(zmq.REQ)
sock.setsockopt(zmq.LINGER, 0)
sock.connect(connectionInfo)

@click.group()
def cli() :
  """CPM CLI - Corpus & Process Manager Command Line Interface"""
  pass

@cli.group()
def process():
  """Manage cpm process"""
  pass

@cli.command()
def reload() :
  """Refresh cpm modules defintion"""
  print com.sendCommand(sock,"reload")

@cli.command()
def log() :
  """Refresh cpm modules defintion"""
  print com.sendCommand(sock,"log")

@cli.command()
def test() :
  """Test command for dev debug purpose"""
  print com.sendCommand(sock,"test")

@cli.command()
def status() :
  """Get information about cpm server status"""
  print com.sendCommand(sock,"status",timeout = 10)

@cli.group()
def corpus() :
  """Depreciated functions (use fs)"""
  pass

@corpus.command()
@click.option("--all","-a",default=False,is_flag=True,help="Print also results")
@click.option("--json",default=False,is_flag=True,help="Print in json format")
def ls(all,json):
  optionall = ""
  optionjson = ""
  if all :
    optionall = " --all"
  if json :
    optionjson = " --json"
  print com.sendCommand(sock,"corpus ls"+optionall+optionjson)

@corpus.command()
@click.argument('filepath')
@click.argument('offset')
def lsdir(filepath,offset):
  print com.sendCommand(sock,"corpus lsdir "+filepath+" "+offset)

@cli.group()
def module() :
  """Manage cpm modules"""
  pass

def modulesls(name):
  return com.sendCommand(sock,"module ls"+name,timeout=10)

def processls(allp):
  return com.sendCommand(sock,"process ls "+allp,timeout=10)
  
def modulehelp(name):
  return com.sendCommand(sock,"module getdesc "+name+" --extended",timeout=10)

def modulefunc(name):
  @cli.command(help=modulehelp(name))
  @click.option('--sync',default=False,is_flag=True,help="Run the module synchronously")
  @click.option('--config','-c',type=click.File('rb'),default=None,help="Yaml environment input configuration file")
  @click.option('--arg',multiple=True,help="Input (overrides configuration file if given) of the form INPUTNAME:VALUE (yaml field format)")
  def func(arg,config,sync):
    confdata = ""
    args = {}
    if config :
      for line in config:
        if line.strip() != "":
          var = line.split(":")
          if len(var) < 2:
            print "Wrong input paramater format : "+line
            return
          paramater = var[0].strip()
          if paramater in args:
            print "warning multiple input values for paramater "+paramater
          args[paramater] = ":".join(var[1:]).strip()

    for item in arg :
      var = item.split(":")
      if len(var) < 2:
        print "Wrong input paramater format : "+item
        return
      paramater = var[0].strip()
      if paramater in args:
        print "warning multiple input values for paramater "+paramater
      args[paramater] = ":".join(var[1:]).strip()

    for paramater in args:
      confdata += paramater+" : "+args[paramater]+"\n"
    synced = ""
    if(sync):
      synced = " --sync"

    print com.sendCommand(sock,"module run "+name+synced,data=confdata)
  return func


def moduleinfofunc(name):
  @cli.command(help=modulehelp(name))
  def func():
    print com.sendCommand(sock,"module info "+name)
  return func








class CPMModulesRun(click.MultiCommand):

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

class CPMModulesInfo(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        modules = modulesls(" --name")
        for filename in modules.split("\n"):
            if filename.strip() != "":
                rv.append(filename)
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        return moduleinfofunc(name)


@cli.command(cls=CPMModulesRun)
def run():
  """Shorthand for "module run" command"""
  pass

  

@module.command()
@click.option('--name', default=False,is_flag=True,help="Only print modules' name")
@click.option('--json', default=False,is_flag=True,help="JSON Format")
def ls(name,json):
  """List all available modules""" 
  optname = ""
  jsonopt = ""
  if name :
    optname = " --name"
  if json :
    jsonopt = " --json"
  print modulesls(optname+jsonopt)


@module.command(cls=CPMModulesInfo)
def info():
  """Get information about a module""" 
  pass

@module.command(cls=CPMModulesRun)
def run():
  """Run a MODULE with configuration file CONF_FILE"""
  pass


@cli.command()
def settings():
  """Retrieve appfm settings"""
  print com.sendCommand(sock,"settings")


@process.command()
def queue():
  print com.sendCommand(sock,"process queue")

@process.command()
@click.option('--all','-a', default=False,is_flag=True,help="List all processes (including stopped/finished processes)")
#@click.option('--recursive','-r', default=False,is_flag=True,help="List also children processes")
@click.option('--head','-h', default=False,is_flag=True,help="List only latest owned")
@click.option('--user','-u', default=False,is_flag=True,help="List only owned processes")
def ls(all,head,user):
  """List running processes"""
  optall = ""
  optrec = ""
  optowned = ""
  if all :
    optall = " -a"
  if head :
    optrec = " -h"
  if user :
    optowned = " -u"
  print com.sendCommand(sock,"process ls"+optall+optrec+optowned)


class CPMProcessActions(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        runs = processls("-a -h")
        for run in runs.split("\n"):
            m = re.search(".*?:\s*([a-zA-Z0-9_\-]+)",run)
            if m:
                rv.append(m.group(1))
        #rv.sort()
        return rv


class CPMProcessView(CPMProcessActions):
  def get_command(self,ctx,name):
    @cli.command()
    @click.argument('outputname',default="__ALL__")
    def processtestview(outputname):
      print com.sendCommand(sock,"process view "+name+" "+outputname)
    return processtestview

@process.command(cls=CPMProcessView)
def view():
  pass

class CPMProcessGet(CPMProcessActions):
  def get_command(self,ctx,pid):
    @cli.command()
    def func():
      print com.sendCommand(sock,"process get "+pid)
    return func

@process.command(cls=CPMProcessGet)
def get():
  """ Print serialized information of a process """
  pass

class CPMProcessStatus(CPMProcessActions):
  def get_command(self,ctx,pid):
    @cli.command()
    def func():
      print com.sendCommand(sock,"process status "+pid)
    return func

@process.command(cls=CPMProcessStatus)
def status():
  """Print the status of a process and its children processes if any"""
  pass

class CPMProcessLog(CPMProcessActions):
  def get_command(self,ctx,pid):
    @cli.command()
    def func():
      print com.sendCommand(sock,"process log "+pid)
    return func

@process.command(cls=CPMProcessLog)
def log():
  """View the default error log of a module run PID"""
  pass

class CPMProcessDel(CPMProcessActions):
  def get_command(self,ctx,pid):
    @cli.command()
    def func():
      print com.sendCommand(sock,"process del "+pid)
    return func

@process.command(cls=CPMProcessDel)
def delete():
  """View the default error log of a module run PID"""
  pass

class CPMProcessKill(CPMProcessActions):
  def get_command(self,ctx,pid):
    @cli.command()
    def func():
      print com.sendCommand(sock,"process kill "+pid)
    return func

@process.command(cls=CPMProcessKill)
def kill():
  """View the default error log of a module run PID"""
  pass


@cli.group()
def fs():
  """Access functions to filesystem (retrieve file, list directories)"""
  pass

@fs.command()
@click.argument('file')
def get(file):
  """Retrieve file content"""
  print com.sendCommand(sock,"fs get "+file)

@fs.command()
@click.argument('directory')
def ls(directory):
  """List directory content"""
  import json
  jsonobj = json.loads(com.sendCommand(sock,"fs ls "+directory+" 0"))
  while "..." in jsonobj[len(jsonobj)-1] :
    jsonobj = jsonobj[:-1]
    jsonobj += json.loads(com.sendCommand(sock,"fs ls "+directory+" "+str(len(jsonobj))))
  print json.dumps(jsonobj)

if __name__ == '__main__':
  cli()
    





