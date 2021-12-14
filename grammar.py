from production import Production


class Grammar:
    def __init__(self, filename):
        self._non_terminals = []
        self._terminals = []
        self._starting_symbol = None
        self._productions = []
        self.read_from_file(filename)

    def getNonTerminals(self):
        return self._non_terminals

    def getTerminals(self):
        return self._terminals

    def getStartSymbol(self):
        return self._starting_symbol

    def getProductions(self):
        return self._productions

    def getProdForNT(self, nonTerm):
        return list(
            filter(
                lambda x: x.getLeft() == nonTerm, self._productions)
        )

    def getProductionByIndex(self, index):
        for p in self._productions:
            if p.getNumber() == int(index):
                    return p

    def read_from_file(self, filename):
        with open(filename, 'r') as file:
            self._non_terminals = file.readline().strip().split(' ')
            self._terminals = file.readline().strip().split(' ')
            self._starting_symbol = file.readline().strip()
            i = 1
            for line in file:
                production = line.strip().split(' ')
                key = production[0].strip()
                values = list(production[2].strip().split('|'))
                for rhs in values:
                    self._productions.append(
                        Production(key, rhs, i)
                    )
                    i += 1

        file.close()
