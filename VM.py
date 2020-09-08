import re
from Opcodes import Opcodes
from Parser import Parser


class VirtualMachine:
    RE_VAR = r"\b[a-z_](\w+|)\b"

    def __init__(self, code):
        self.code = code
        self.line = 0

        self.opcodes = Opcodes(self)
        self.procedures = {
            **Parser.init_procedures
        }

        self.vars = dict()
        self.stack = []
        self.jmp_stack = []
        self.labels = dict()

    def parse_label(self, label, exception=True):
        if label in self.labels:
            return self.labels[label]
        elif exception:
            raise Exception(f"Unknown label: {label}")

    def parse_var(self, var, exception=True):
        return var[0]

    def parse_value(self, value, exception=True):
        if isinstance(value, list):
            return self.vars[value[0]]
        return value

    def parse_labels(self):
        for i, line in enumerate(self.code):
            if isinstance(line, str):
                self.labels[line] = i

    def run(self):
        opcodes = {v: k for k, v in Parser.opcodes.items()}
        self.parse_labels()
        self.line = self.labels["main"]
        while self.line < len(self.code):
            line = self.code[self.line]
            if isinstance(line, list):
                self.opcodes.__getattribute__(opcodes[line[0]])(self.line, line[1])
            self.line += 1
        print(self.vars)
        print(self.stack)
