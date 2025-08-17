from collections import defaultdict


class LineInfo:
    def __init__(self):
        self.infos = defaultdict(list)
        self.counter = 1

    def add_info(self, info):
        self.infos[self.counter].append(info)

    def add_counter(self, count):
        self.counter += count

    def format_to_text2(self):
        text = ""
        for counter, infos in sorted(self.infos.items()):
            for info in infos:
                text += "#" + str(counter) + " : syntax error, " + info + "\n"
        return text

    def format_to_text(self):
        text = ""
        for counter, infos in sorted(self.infos.items()):
            text += str(counter) + ".\t"
            for info in infos:
                text += info + " "
            text += "\n"
        return text
