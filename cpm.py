#!/usr/bin/python

import sys
import zmq
import os

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

@cli.command()
def reload() :
  """Refresh cpm modules defintion"""
  print com.sendCommand(sock,"reload")

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
def ls(name):
  """List all available modules""" 
  optname = ""
  if name :
    optname = " --name"
  print modulesls(optname)


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
  print com.sendCommand(sock,"process ls"+optall+optrec)

@process.command()
@click.argument('pid')
def get(pid):
  """ Print serialized information of a process """
  print com.sendCommand(sock,"process get "+pid)

@process.command()
@click.argument('pid')
def status(pid):
  """Print the status of a process and its children processes if any"""
  print com.sendCommand(sock,"process status "+pid)

@process.command()
@click.argument('pid')
@click.argument('outputname',default="__ALL__")
@click.option('--gui','-g',default=False,is_flag=True,help="View graphical result in a browser")
def view(pid,outputname,gui):
  """View the output OUTPUTNAME of a module run PID"""
  optgui = ""
  if gui :
    optgui = " --gui"
  res = com.sendCommand(sock,"process view "+pid+" "+outputname+optgui)
  if gui :
    webbrowser.open(guihost+res)
  else :
    print res

@process.command()
@click.argument('pid')
@click.option('--gui','-g',default=False,is_flag=True)
def log(pid,gui):
  """View the default error log of a module run PID"""
  res = com.sendCommand(sock,"process log "+pid)
  print res


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
    





