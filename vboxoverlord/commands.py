from __future__ import print_function
from util import *


class Commands(object):
    def __init__(self, vbo):
        self.vbo = vbo

    def __call__(self, cmd, *args):
        try:
            print_list(getattr(self,cmd)(*args))
        except Exception as e:
            print(e)
            print("Command '{0}' failed :(".format(cmd))

    def vms(self, *args):
        """
        Command Function to print out a formatted list of all VMs on all servers
        """
        return get_all_vms(self.vbo)

    def runningvms(self, *args):
        """
        Command function to print out a formattted list of all running VMs on
        all servers
        """
        return get_running_vms(self.vbo)

    def stoppedvms(self, *args):
        """
        Command function to print out a formatted list of all stopped VMS on all
        servers
        """
        running = get_running_vms(self.vbo)
        allvms = get_all_vms(self.vbo)
        return filter(lambda vm: vm not in running, allvms)

    def whereis(self, *args):
        """
        Command function to display which host a VM is on
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
        Command to return a list of all servers we know about
        """
        return [s for s in self.vbo.servers]


    def forcestop(self, *args):
        """
        Command to forcefully power off a VM
        """
        vm_name = ' '.join(args)
        host = get_vm_host(self.vbo, vm_name)
        if host:
            return host.force_stop(vm_name)

    def stop(self, *args):
        """
        Command to Stop a given VM
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
        Command to start a vm
        """
        vm_name = ' '.join(args)
        host = get_vm_host(self.vbo, vm_name)
        if host:
            host.start_vm(vm_name)
            return "Started VM {0}"
        else:
            return "VM {0} not found"


    def exit(self, *args):
        """
        Exit command, forwards directly to the Overlord.exit() function
        """
        self.vbo.exit()


