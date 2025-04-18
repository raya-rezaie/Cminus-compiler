class CharReader:
    def __init__(self, filepath):
        self.file = open(filepath, 'r', encoding='utf-8')
        self.eof_reached = False

    def read(self):
        # if self.eof_reached:
        #     return 'EOF'
        
        char = self.file.read(1) 
        # if char == '':
        #     self.eof_reached = True
        #     self.file.close()
        #     return 'EOF'
        return char

    def back(self):
        # if self.eof_reached:
        #     self.eof_reached = False
        #     self.file = open(self.file.name, 'r')
        #     self.file.seek(self.file_size - 1)
        # else:
        pos = self.file.tell()
        if pos > 0:
            self.file.seek(pos - 1)