import pickle
from VM import VirtualMachine
from Compiler import Compiler


c = Compiler("byte_code.ss")
c.run()

with open("byte_code.ssb", "rb") as f:
    vm = VirtualMachine(pickle.load(f))
vm.run()
