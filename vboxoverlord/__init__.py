import paramiko
import ConfigParser
from getpass import getpass
from functools import partial


class SuperParamiko(object):
    def __init__(self, host, username, password=None, port=22):
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
        if password == None:
            self.session.connect(host, username=username, port=port)
        else:
            self.session.connect(
                    host,
                    username=username,
                    password=password,
                    port=port
            )

    def generate_command_string(self, cmd, *args, **kwargs):
        command = [cmd,]
        command.extend(list(args))
        for key, arg in kwargs.items():
            if arg == None or arg == "":
                command.append("--{0}".format(key))
            else:
                command.append("--{0} {1}".format(key, arg))
        return ' '.join(command)

    def ssh_func_wrapper(self, cmd, *args, **kwargs):
        command = self.generate_command_string(cmd, *args, **kwargs)
        stdin, stdout, stderr = self.session.exec_command(command)
        errors = stderr.readlines()
        if errors != []:
            raise Exception(errors)
        else:
            return map(lambda s: s.strip(), stdout.readlines())

    def __getattr__(self, name):
        return partial(self.ssh_func_wrapper, name)


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
    def __init__(self, config_path):
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_path)
        print self.config
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

    def getServers(self):
        return [s for s in self.servers]

    def getAllVMs(self):
        things = []
        for key in self.servers:
            things.append("----{0}----".format(key))
            vms = self.servers[key].getVMs()
            things.extend(vms)
        return things


    def getAllRunningVMs(self):
        things = []
        for key in self.servers:
            things.append("---{0}---".format(key))
            vms = self.servers[key].getRunningVMs()
            things.extend(vms)
        return things

    def raw(self, server, *args):
        try:
            print '\n'.join(self.servers[server].raw(*args))
        except KeyError:
            print "Server: '{0}' does not exist".format(server)

    def handle_input(self, cmd):
        cmd_list = cmd.split(" ")
        if cmd_list[0] == "vms":
            print '\n'.join(self.getAllVMs())
        elif cmd_list[0] == "runningvms":
            print '\n'.join(self.getAllVMs())
        elif cmd_list[0] == "exit":
            exit()
        elif cmd_list[0] == "servers":
            print '\n'.join(self.getServers())

        else:
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
                print "VM '{0}' not found".format(server)

def rpel():
    import os.path
    overlord = Overlord(os.path.expanduser("~/.config/vboxoverlord.conf"))
    while True:
        try:
            overlord.handle_input(raw_input(">> "))
        except EOFError:
            exit()
        except KeyboardInterrupt:
            continue
        print ""
