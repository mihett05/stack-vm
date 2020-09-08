import re
import procedures
from Opcodes import Opcodes


class Parser:
    RE_VAR = r"\b[a-z_](\w+|)\b"
    init_procedures = {
        "print": procedures.cb_print,
        "itos": procedures.itos
    }
    opcodes = {v: i for i, v in enumerate(filter(lambda x: not x.startswith("_"), Opcodes.__dict__))}

    def __init__(self, code):
        self.code = code
        self._line = 0

        self.vars = dict()  # name: index
        self.labels = []

    def parse_var(self, var, exception=True):
        if re.findall(self.RE_VAR, var):
            return var
        elif exception:
            raise Exception(f"Line: {self._line + 1}: Incorrect name of var {var}")
        else:
            return None

    def parse_value(self, value, exception=True):
        if isinstance(value, str):
            if value.isdigit():
                return int(value)
            elif value in self.labels:
                return value
            elif value in self.init_procedures:
                return list(self.init_procedures.keys()).index(value)
            elif len(value) >= 3 and value.startswith("'") and value.endswith("'"):
                return ord(value[1:-1].replace("\\n", "\n").replace("\\r", "\r").replace("\\t", "\t"))
            var = self.parse_var(value, exception=exception)
            if var in self.vars:
                return [self.vars[var]]
            elif exception:
                raise Exception(f"Line: {self._line + 1}: Unknown var {var}")
            else:
                return None
        return value

    def parse_labels(self):
        for line in self.code.split("\n"):
            point = re.findall(r"^\s*(\w+):\s*$", line)
            if len(point) > 0:
                self.labels.append(point[0])

    def parse(self):
        ops = []
        self.parse_labels()
        for self._line, line in enumerate(self.code.split("\n")):
            opcodes = re.findall(r"^\s*(\w+)(\s+(.*)|)\s*$", line)
            if opcodes:
                op = opcodes[0][0]
                args = list(re.split(r",\s+", opcodes[0][2]))
                if op in ["mov", "pop", "arr_new"]:
                    if args[0] not in self.vars:
                        self.vars[args[0]] = 0 if len(self.vars.values()) == 0 else max(self.vars.values()) + 1
                for i, arg in enumerate(args):
                    args[i] = self.parse_value(arg)
                ops.append([self.opcodes[op], args])
            point = re.findall(r"^\s*(\w+):\s*$", line)
            if len(point) > 0:
                ops.append(point[0])
        return ops
