def opcode(args_count):
    def decorator(func):
        def wrapper(self, line, args):
            if len(args) == args_count:
                return func(self, line, args)
            else:
                raise Exception(f"Line: {line}: Operator {func.__name__} takes only {args_count} args")
        return wrapper
    return decorator


class Opcodes:
    def __init__(self, vm):
        self.vm = vm

    @opcode(2)
    def mov(self, line, args):
        self.vm.vars[self.vm.parse_var(args[0])] = self.vm.parse_value(args[1])

    @opcode(1)
    def push(self, line, args):
        value = self.vm.parse_value(args[0])
        self.vm.stack.append(value)

    @opcode(1)
    def pop(self, line, args):
        var = self.vm.parse_var(args[0])
        self.vm.vars[var] = self.vm.stack.pop()

    @opcode(1)
    def jmp(self, line, args):
        jmp_line = self.vm.parse_label(args[0])
        self.vm.jmp_stack.append(self.vm.line)
        self.vm.line = jmp_line

    @opcode(1)
    def je(self, line, args):
        if self.vm.stack.pop():
            self.jmp(line, args)

    @opcode(1)
    def jne(self, line, args):
        if not self.vm.stack.pop():
            self.jmp(line, args)

    @opcode(1)
    def ne(self, line, args):
        value = self.vm.parse_value(args[0])
        self.vm.stack.append(not value)

    @opcode(2)
    def lt(self, line, args):
        left = self.vm.parse_value(args[0])
        right = self.vm.parse_value(args[1])
        self.vm.stack.append(int(left < right))

    @opcode(2)
    def add(self, line, args):
        left = self.vm.parse_value(args[0])
        right = self.vm.parse_value(args[1])
        self.vm.stack.append(left + right)

    @opcode(2)
    def sub(self, line, args):
        left = self.vm.parse_value(args[0])
        right = self.vm.parse_value(args[1])
        self.vm.stack.append(left - right)

    @opcode(2)
    def mul(self, line, args):
        left = self.vm.parse_value(args[0])
        right = self.vm.parse_value(args[1])
        self.vm.stack.append(left * right)

    @opcode(2)
    def div(self, line, args):
        left = self.vm.parse_value(args[0])
        right = self.vm.parse_value(args[1])
        self.vm.stack.append(left / right)

    def ret(self, line, args):
        self.vm.line = self.vm.jmp_stack.pop()

    @opcode(1)
    def arr_new(self, line, args):
        var = self.vm.parse_var(args[0])
        self.vm.vars[var] = []

    @opcode(2)
    def arr_push(self, line, args):
        arr = self.vm.parse_value(args[0])
        value = self.vm.parse_value(args[1])
        arr.append(value)

    @opcode(1)
    def arr_pop(self, line, args):
        arr = self.vm.parse_value(args[0])
        self.vm.stack.append(arr.pop())

    @opcode(2)
    def arr_get(self, line, args):
        arr = self.vm.parse_value(args[0])
        index = self.vm.parse_value(args[1])
        self.vm.stack.append(arr[index])

    @opcode(3)
    def arr_set(self, line, args):
        arr = self.vm.parse_value(args[0])
        index = self.vm.parse_value(args[1])
        value = self.vm.parse_value(args[2])
        arr[index] = value

    @opcode(1)
    def call(self, line, args):
        proc_name = list(self.vm.procedures.keys())[args[0]]
        self.vm.procedures[proc_name](self.vm)
