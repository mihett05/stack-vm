from VM import VirtualMachine


with open("byte_code.txt", "r") as f:
    vm = VirtualMachine(f.read())
vm.run()
