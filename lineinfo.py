from collections import defaultdict

class LineInfo:
    def __init__(self):
        self.infos = defaultdict(list)
        self.counter = 1

    def add_info(self, info):
        self.infos[self.counter].append(info)
    
    def add_counter(self):
        self.counter += 1

    def format_to_text(self):
        text = ""
        for counter, infos in sorted(self.infos.items()):
            text += str(counter) + ".\t"
            for info in infos:
                text += info + " "
            text += "\n"
        return text