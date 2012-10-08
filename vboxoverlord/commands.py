from __future__ import print_function
from util import *
from string import strip
import inspect


class Commands(object):
    def __init__(self, vbo):
        self.vbo = vbo

    def __call__(self, cmd, *args):
        try:
            result = getattr(self,cmd)(*args)
            if type(result) == type(""):
                print_list([result])
            else:
                print_list(result)
        except Exception as e:
            print(e)
            print("Command '{0}' failed :(".format(cmd))

    def vms(self, *args):
        """
        vms [] Print out all VMs on every server
        """
        return get_all_vms_formatted(self.vbo)

    def runningvms(self, *args):
        """
        runningvms [] Print out all running VMs on every server
        """
        return get_all_running_vms_formatted(self.vbo)

    def stoppedvms(self, *args):
        """
        stoppedvms [] Print out all stopped VMs on every server
        """
        running = get_all_running_vms(self.vbo)
        allvms = get_all_vms(self.vbo)
        return filter(lambda vm: vm not in running, allvms)

    def whereis(self, *args):
        """
        whereis [VM_NAME] Print out which server a VM is on
        """
        if len(args) < 1:
            return "Error, whereis takes a VM name as an argument"
        else:
            vm_name = ' '.join(list(args))
            hosts = filter(lambda vbox: vm_name in vbox.get_vm_names(),
                self.vbo.servers.values())
            try:
                return ["'{0} is on '{1}'".format(vm_name, hosts[0].host)]
            except IndexError:
                return ["'{0}' not found".format(vm_name)]

    def servers(self, *args):
        """
        servers [] Print out a list of VBox servers we can control
        """
        return [s for s in self.vbo.servers]


    def forcestop(self, *args):
        """
        forcestop [VM_NAME] Pull the plug on a VM, essentially forcing it offline
        """
        vm_name = ' '.join(args)
        host = get_vm_host(self.vbo, vm_name)
        if host:
            return host.force_stop(vm_name)

    def stop(self, *args):
        """
        stop [VM_NAME] Ask the VM to shutdown nicely as opposed to forcefully powering it off
        """
        vm_name = ' '.join(args)
        host = get_vm_host(self.vbo, vm_name)
        if host:
            return host.stop(vm_name)
        host = get_vm_host(self.vbo, vm_name)
        if host:
            return host.co

    def start(self, *args):
        """
        start [VM_NAME] Turn the specified VM on (This does so in headless mode)
        """
        vm_name = ' '.join(args)
        host = get_vm_host(self.vbo, vm_name)
        if host:
            host.start_vm(vm_name)
            return "Started VM {0}".format(vm_name)
        else:
            return "VM {0} not found".format(vm_name)

    def init(self, *args):
        """
        init [start | stop | add | remove] [level] (VM_NAMES) Handle the VM init level system
            init start     [level] Start the specified init level
            init stop      [level] Force stop the specified init level
            init add       [level] [VM_NAME] Add the specified VM to the specified level
            init remove    [level] [VM_NAME] Remove the specified VM from the specified level
        """
        sub_command = args[0]
        if sub_command == "add" or sub_command == "remove":
            level = args[1]
            vm_name = " ".join(args[2:])
            if sub_command == "add":
                result = self.vbo.add_init(level, vm_name)
                if result:
                    return "Added '{0}' to init level {1}".format(
                            vm_name,
                            level)
                else:
                    return "Failed to add {0} to init level {1}".format(
                            vm_name,
                            level)
            if sub_command == "remove":
                result = self.vbo.remove_init(level, vm_name)
                if result:
                    return "Removed '{0}' from init level {1}".format(
                            vm_name,
                            level)
                else:
                    return "Failed to remove '{0}' from init level {1}".format(
                            vm_name,
                            level)
                if sub_command == "start" or sub_command == "stop":
                    level = args[1]
                    if sub_command == "stop":
                        vms_to_stop = self.vbo.init_levels[level]
                        output = []
                        for vm in vms_to_stop:
                            host = get_vm_host(self.vbo, vm)
                            result = host.force_stop(vm)
                            output.append(result)
                        output.append("Immediate shutdown of init level {0} complete".format(level))
                        return output
                    if sub_command == "start":
                        vms_to_start = self.vbo.init_levels[level]
                        output = []
                        for vm in vms_to_start:
                            host = get_vm_host(self.vbo, vm)
                            result = host.start(vm)
                            output.append(result)
                        output.append("Startup of init level {0} complete".format(level))


    def help(self, *args):
        """
        Display the overall help menu or provide specific info on a command
        """
        if len(args) > 0:
            cmd = args[0]
            try:
                cmd_func = getattr(self, cmd)
                return map(strip, cmd_func.__doc__.split("\n"))
            except:
                return "That command doesn't exist"
        else:
            help_text = [
                    "VirtualBox Overlord:",
                    "Use help [cmd] for more specific information",
                    ]
            func_names = map(lambda x: '\t' + x[0],filter(lambda e: not e[0].startswith("__"),
                    inspect.getmembers(self)))
            help_text.extend(func_names)
            return help_text




    def exit(self, *args):
        """
        Exit command, forwards directly to the Overlord.exit() function
        """
        self.vbo.exit()


