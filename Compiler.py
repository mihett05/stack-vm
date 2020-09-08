import pickle

from Parser import Parser


class Compiler:
    def __init__(self, filename: str):
        self.filename = filename
        with open(filename, "r") as f:
            self.code = f.read()
        self.parser = Parser(self.code)

    def run(self):
        with open(f"{self.filename.split('.')[:-1][0]}.ssb", "wb") as f:
            pickle.dump(self.parser.parse(), f)
