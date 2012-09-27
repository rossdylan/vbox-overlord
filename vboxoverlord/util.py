from __future__ import print_function
from itertools import chain
import ConfigParser
import os
import os.path

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


def write_default_config():
    """
    Check to see if there is a preexisting config file and if there isn't make
    a new one with the proper defaults
    """
    if os.path.exists(os.path.expanduser("~/.config/vboxoverlord/vbo.conf")):
        return
    else:
        if not os.path.exists(os.path.expanduser("~/.config/vboxoverlord/")):
            os.makedir(os.path.expanduser("~/.config/vboxoverlord"))
        config = {
                "global": {
                    "username": "vm",
                    "port": 22,
                    },
                "servers": {
                    "local": "localhost",
                    },
                "init_levels": {
                    "1": "",
                    "2": "",
                    "3": "",
                    "4": "",
                    "5": "",
                    },
                }
        write_config(config)


def write_config(config_dict):
    """
    Write a dict with config options out to the config file
    """
    with open(os.path.expanduser("~/.config/vboxoverlord/vbo.conf"),'wb') as f:
        config = ConfigParser.RawConfigParser()
        for section in config_dict:
            config.add_section(section)
            for key in config_dict[section]:
                config.set(section, key, config_dict[section][key])
        config.write(f)


def build_init_levels(config):
    """
    Take the init levels as defined by the config file and turn them into a dict
    that we can make sense of and use
    """
    init_dict = {}
    for x in xrange(1,6):
        init_str = config.get("init_levels", str(x))
        if init_str == "":
            init_dict[str(x)] = []
        else:
            init_dict[str(x)] = [v.strip() for v in init_str.split(",")]



