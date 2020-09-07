import re
import procedures


class VirtualMachine:
    RE_VAR = r"\b[a-z_](\w+|)\b"

    def __init__(self, byte_code: str):
        self.code = byte_code
        self.line = 0

        self.opcodes = Opcodes(self)

        self.vars = dict()
        self.procedures = {
            "print": procedures.cb_print,
            "itos": procedures.itos
        }
        self.stack = []
        self.jmp_stack = []
        self.labels = dict()

    def parse_var(self, var, exception=True):
        if re.findall(self.RE_VAR, var):
            return var
        elif exception:
            raise Exception(f"Line: {self.line}: Incorrect name of var {var}")
        else:
            return None

    def parse_value(self, value, exception=True):
        if isinstance(value, str):
            if len(value) >= 3 and value.startswith("'") and value.endswith("'"):
                return ord(value[1:-1].replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t"))
            # elif len(value) >= 2 and value.startswith("\"") and value.endswith("\""):
            #     return list(
            #         value[1:-1].replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t")
            #     )
            var = self.parse_var(value, exception=exception)
            if var in self.vars:
                return self.vars[var]
            elif exception:
                raise Exception(f"Line: {self.line}: Unknown var {var}")
            else:
                return None
        return value

    def parse_label(self, name, exception=True):
        if isinstance(name, str):
            if name in self.labels:
                return self.labels[name]
        if exception:
            raise Exception(f"Line: {self.line}: Unknown label {name}")
        else:
            return None

    def parse_labels(self):
        for i, line in enumerate(self.code.split("\n")):
            point = re.findall(r"^\s*(\w+):\s*$", line)
            if len(point) > 0:
                self.labels[point[0]] = i

    def run(self):
        self.parse_labels()
        lines = self.code.split("\n")
        self.line = self.labels["main"]
        while self.line < len(lines):
            opcodes = re.findall(r"^\s*(\w+)(\s+(.*)|)\s*$", lines[self.line])
            if opcodes:
                args = list(re.split(r",\s*", opcodes[0][2]))
                for i, arg in enumerate(args):
                    if arg.isdigit():
                        args[i] = int(arg)
                name = opcodes[0][0]
                if hasattr(self.opcodes, name):
                    self.opcodes.__getattribute__(name)(self.line, args)
                else:
                    raise Exception(f"Line: {self.line}: Unknown operation {name}")
            self.line += 1
        print(self.vars)
        print(self.stack)


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
    def __init__(self, vm: VirtualMachine):
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
        proc_name = self.vm.parse_var(args[0])
        self.vm.procedures[proc_name](self.vm)
