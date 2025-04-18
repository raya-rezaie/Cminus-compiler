from automata import *
from main import *
class LineReader:
    def __init__(self, filepath):
        self.file = open(filepath, 'r')
        self.line_number = 0

    def __call__(self):
        line = self.file.readline()
        if not line:
            self.file.close()
            raise StopIteration("End of file reached")
        self.line_number += 1
        return self.line_number, line.rstrip('\n')

reader = LineReader('test.txt')

