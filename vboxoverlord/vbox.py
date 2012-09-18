from SuperParamiko import SuperParamiko

class VboxServer(object):
    def __init__(self, host, port, user, password):
        self.host = host
        self.connection = SuperParamiko(
                host,
                user,
                password = password,
                port = port
        )

    def get_vm_names(self):
        vm_names = map(lambda vm: vm.split(" ")[0].replace('"', ""), self.get_vms())
        return vm_names

    def control_vm(self, VM, option):
        return self.connection.vboxmanage("controlvm", VM, option)

    def start_headless(self, VM):
        return self.connection.vboxmanage("startvm", VM, type="headless")

    def force_stop(self, VM):
        return self.control_vm(VM, "poweroff")

    def stop(self, VM):
        return self.control_vm(VM, "acpipowerbutton")

    def pause(self, VM):
        return self.contro_vm(VM, "pause")

    def resume(self, VM):
        return self.control_vm(VM, "resume")

    def get_vms(self):
        return self.connection.vboxmanage("list", "vms")

    def get_running_vms(self):
        return self.connection.vboxmanage("list", "runningvms")

    def raw(self, *args):
        return self.connection.vboxmanage(*args)


