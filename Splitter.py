import re


class Splitter:
    def __init__(self, text_to_be_parsed):
        self._words = text_to_be_parsed
        self._splitted = re.split('(\+|-|\*|/|:=|<=|<|>=|>|:|;)', self._words)
        for i in range(len(self._splitted)):
            self._splitted[i]=self._splitted[i].strip()

        self._tokens = {}
        f = open("token.in", 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split()
            self._tokens[line[0].upper()] = line[1]
        self.extract_constants()

    def get_splitted(self):
        return self._splitted

    def extract_constants(self):
        hehe=[]
        for i in self._splitted:
            elements=re.split('(\".*\"|[0-9]+)',i)
            for e in elements:
                if not re.findall('\".*\"'
                                  '',e):
                    e=re.split('(,|\(|\)|]|\[)',e)
                    for elem in e:
                        if elem.split() != []:
                             hehe.extend(elem.split() )
                else:
                    hehe.append(e)
        self._splitted=hehe


    def print_splitted(self):
        for i in self._splitted:
            print(i.strip())



