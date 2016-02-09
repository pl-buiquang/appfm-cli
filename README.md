== AppFM Command Line Interface

This python script/package allow command line interaction with AppFM. Documentation of the availables commands are inlined in the application.
Just type (after proper installation) : cpm --help
More information is provided in the wiki (within the web interface of an existing installation)

== Installation

=== Install python module
[code]pip install .[/code]

(if used "--user", make sure ~/.local/bin or wherever pip installed cpm script is in you $PATH)

=== Set up autocompletion
add [code]eval "$(_CPM_COMPLETE=source cpm)"[/code]

or

[code]./genrate-autocomplete.sh[/code]

then add ". {/path/to/}cpm-complete.sh" to your bash, to prevent login overhead

=== Edit configuration file

There is as yet no configuration file. To change the server information you have to edit the variables "serverhost" and "serverport" in the source file "cpm.py".

== TODO

add default behavior to cpm process status (check last master process run) and perhaps others
