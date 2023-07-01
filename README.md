# AppFM Command Line Interface

This python script/package allow command line interaction with AppFM. Documentation of the availables commands are inlined in the application.
Just type (after proper installation) : cpm --help
More information is provided in the wiki (within the web interface of an existing installation)

## Dependencies

This python module requires python-dev and python-pip to be installed on the system. If this is not the case, you can install them by typing :
sudo apt-get install python-dev python-pip

## Quick install

Be sure that the current working directory is the one containing this file then execute :
```
./install.sh
```

## Manual Installation

### Install python module
```
pip install .
```

(if used "--user", make sure ~/.local/bin or wherever pip installed cpm script is in you $PATH)

### Set up autocompletion
add 
```
eval "$(_CPM_COMPLETE=source cpm)"
```

or

```
./genrate-autocomplete.sh
```

then add ". {/path/to/}cpm-complete.sh" to your bash, to prevent login overhead

### Edit configuration file

There is as yet no configuration file. To change the server information you have to edit the variables "serverhost" and "serverport" in the source file "cpm.py".

## TODO

add default behavior to cpm process status (check last master process run) and perhaps others
