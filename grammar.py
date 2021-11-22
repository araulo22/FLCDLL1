class Grammar:
    def __init__(self, filename):
        self._non_terminals=[]
        self._terminals=[]
        self._starting_symbol=None
        self._productions= {}
        self.read_from_file(filename)

    def read_from_file(self, filename):
            with open(filename,'r') as file:
                self._non_terminals=file.readline().strip().split(' ')
                self._terminals=file.readline().strip().split(' ')
                self._starting_symbol=file.readline().strip()
                for line in file:
                    production = line.strip().split(' ')
                    ok=0
                    key = production[0].strip()
                    values = list(production[2].strip().split('|'))
                    for value in values:
                        if key in self._productions:
                            self._productions[key].append(value)
                        else:
                            self._productions[key]=[value]
            file.close()



g=Grammar('grammar1.txt')
print(g._productions)