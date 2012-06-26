vbox-overlord
=============

managment system for multiple virtualbox servers

Config File
===========
Add your servers to ~/.config/vboxoverlord/vbo.conf

Command structure:
=================

whereis <vmname>
- Returns the server that VM is located on

<servername> <command>
- run the command on the specified server

<vmname> <command>
- same as above
- NOTE: if the name of the vm is needed within the command, you will need to add
  it in, the vmname only acts as an alias for the server

vms
- returns all vms across all machines

runningvms
- returns all running vm's across all machines

