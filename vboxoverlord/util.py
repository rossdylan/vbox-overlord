from __future__ import print_function
from itertools import chain
__all__ = [
    'get_all_vms',
    'get_all_vms_formatted',
    'get_all_running_vms_formatted',
    'get_all_running_vms',
    'get_all_vms',
    'get_vm_host',
    'print_list']

def get_all_vms_formatted(vbo):
    """
    Return all VMs on all servers
    """

    return chain.from_iterable(
            map(
                lambda vbox: ["-----{0}----".format(vbox.host),] + vbox.get_vms(),
                vbo.servers.values()
                )
            )

def get_all_vms(vbo):
    return chain.from_iterable(
            [vbox.get_all_vms() for vbox in vbo.servers.values()])

def get_all_running_vms(vbo):
    return chain.from_iterable(
            [vbox.get_running_vms() for vbox in vbo.servers.values()])

def get_all_running_vms_formatted(vbo):
    """
    Get All running VMs on all servers
    """

    return chain.from_iterable(
            map(
                lambda vbox: ["----{0}----".format(vbox.host),] + vbox.get_running_vms(),
                vbo.servers.values()
                )
            )

def get_vm_host(vbo, vm_name):
    """
    Get the VM host that a VM is on
    """

    try:
        return filter(lambda vbox: vm_name in vbox.get_vm_names(),
                vbo.servers.values())[0]
    except IndexError:
        return None

def print_list(l):
    print('\n'.join(l))


