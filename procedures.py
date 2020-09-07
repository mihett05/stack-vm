def cb_print(vm):
    arr = vm.stack.pop()
    print("".join(map(chr, arr)), sep="", end="")


def itos(vm):
    num = vm.stack.pop()
    vm.stack.append(list(map(ord, str(num))))

