from getpass import getpass
from vbox import VboxServer
from commands import Commands
from util import write_default_config, build_init_levels
import readline
import ConfigParser
import os
import os.path


class Overlord(object):
    def __init__(self):
        write_default_config()
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.expanduser("~/.config/vboxoverlord/vbo.conf"))
        self.username = self.config.get("global", "username")
        self.port = self.config.getint("global", "port")
        self.password = getpass("Enter global VM user password: ")
        self.init_levels = build_init_levels(self.config)
        self.init_levels_changed = False
        # Used to tell if we modified the init levels
        self.commands = Commands(self)
        try:
            temp = map(
                lambda item: VboxServer(
                    item[1],
                    self.port,
                    self.username,
                    self.password
                    ),
                self.config.items("servers")
                )
        except:
            print("Failed to connect to hosts")
            self.exit()
        self.servers = {}
        for server in temp:
            self.servers[server.host] = server

    def add_init(self, level, vm_name):
        """
        Add a machine to an init level
        Returns false if machine is already in an init level
        """
        if level not in self.init_levels:
            return False

        for level in self.init_levels:
            if vm_name in level:
                return False

        self.init_levels[str(level)].append(vm_name)
        self.init_levels_changed = True
        return True

    def remove_init(self, level, vm_name):
        """
        Remove a machine from an init level
        Returns false if the machine isn't in the specified init_level
        """
        if level not in self.init_levels:
            return False

        try:
            self.init_levels['level'].remove(vm_name)
            self.init_levels_changed = True
            return True
        except:
            return False

    def exit(self):
        """
        Write out the config file (assuming something has changed and exit()
        """
        #TODO check init levels and make sure we don't need to update the config
        if self.init_levels_changed:
            self.config.add_section("init_levels")
            for level in self.init_levels:
                self.config.set("init_levels", level, self.init_levels[level])
        self.config.write(open(os.path.expanduser("~/.config/vboxoverlord/vbo.conf"),'w'))
        exit()

    def handle_input(self, cmd):
        cmd_list = cmd.split(" ")
        self.commands(cmd_list[0], *tuple(cmd_list[1:]))


def rpel():
    readline.parse_and_bind("tab: complete")
    overlord = Overlord()
    while True:
        try:
            overlord.handle_input(raw_input(">> "))
        except EOFError:
            overlord.exit()
        except KeyboardInterrupt:
            continue
        print("")
