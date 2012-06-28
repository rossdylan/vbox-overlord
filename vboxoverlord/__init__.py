from __future__ import print_function
import ConfigParser
import os
import os.path
from getpass import getpass
from SuperParamiko import SuperParamiko
from itertools import chain

def write_config():
    if os.path.exists(os.path.expanduser("~/.config/vboxoverlord/vbo.conf")):
        return
    else:
        if not os.path.exists(os.path.expanduser("~/.config/vboxoverlord/")):
            os.mkdir(os.path.expanduser("~/.config/vboxoverlord"))
        with open(os.path.expanduser("~/.config/vboxoverlord/vbo.conf"),'wb') as f:
            config = ConfigParser.RawConfigParser()
            config.add_section('global')
            config.set('global', 'username', 'vm')
            config.set('global', 'port', 22)
            config.add_section('servers')
            config.set('servers', 'local', 'localhost')
            config.write(f)

def print_list(l):
    print('\n'.join(l))

class VboxServer(object):
    def __init__(self, host, port, user, password):
        self.host = host
        self.connection = SuperParamiko(
                host,
                user,
                password = password,
                port = port
        )

    def getVMNames(self):
        vm_names = map(lambda vm: vm.split(" ")[0].replace('"', ""), self.getVMs())
        return vm_names

    def controlVM(self, VM, option):
        return self.connection.vboxmanage("controlvm", option, VM)

    def startHeadless(self, VM):
        return self.connection.vboxmanage("startvm", VM, type="headless")

    def getVMs(self):
        return self.connection.vboxmanage("list", "vms")

    def getRunningVMs(self):
        return self.connection.vboxmanage("list", "runningvms")

    def raw(self, *args):
        return self.connection.vboxmanage(*args)


class Overlord(object):
    def __init__(self):
        write_config()
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.expanduser("~/.config/vboxoverlord/vbo.conf"))
        self.username = self.config.get("global", "username")
        self.port = self.config.getint("global", "port")
        self.password = getpass("Enter global VM user password: ")
        temp = map(
            lambda item: VboxServer(
                item[1],
                self.port,
                self.username,
                self.password
                ),
            self.config.items("servers")
            )
        self.servers = {}
        for server in temp:
            self.servers[server.host] = server
        self.commands = {
            "vms": lambda args: print_list(self.getAllVMs()),
            "runningvms": lambda *args: print_list(self.getRunningVMs()),
            "servers": lambda *args: print_list(self.getServers()),
            "whereis": lambda *args: print(
                self.whereis(' '.join(list(*args)))
                ),
            "exit": lambda *args: exit()
            }


    def getServers(self):
        return [s for s in self.servers]

    def getAllVMs(self):
        return chain.from_iterable(
                map(
                    lambda vbox: ["----{0}----".format(vbox.host),] + vbox.getVMs(),
                    self.servers.values()
                    )
                )


    def getRunningVMs(self):
        return chain.from_iterable(
                map(
                    lambda vbox: ["----{0}----".format(vbox.host),] + vbox.getRunningVMs(),
                    self.servers.values()
                    )
                )

    def raw(self, server, *args):
        try:
            print_list(self.servers[server].raw(*args))
        except KeyError:
            print("Server: '{0}' does not exist".format(server))

    def whereis(self, vm_name):
        hosts = filter(lambda vbox: vm_name in vbox.getVMNames(),
                self.servers.values())
        try:
            return "'{0} is on '{1}'".format(vm_name, hosts[0].host)
        except IndexError:
            return "'{0}' not found".format(vm_name)


    def handle_input(self, cmd):
        cmd_list = cmd.split(" ")
        try:
            self.commands[cmd_list[0]](tuple(cmd_list[1:]))
        except KeyError:
            server = cmd_list[0]
            if server in self.servers:
                args = tuple(cmd_list[1:])
                self.raw(server, *args)
            else:
                # Server is assumed to be a vm name now
                for key in self.servers:
                    vbox = self.servers[key]
                    if server in vbox.getVMNames():
                        args = tuple(cmd_list[1:])
                        self.raw(vbox.host, *args)
                        return
                print("VM '{0}' not found".format(server))

def rpel():
    overlord = Overlord()
    while True:
        try:
            overlord.handle_input(raw_input(">> "))
        except EOFError:
            exit()
        except KeyboardInterrupt:
            continue
        print("")
