from production import Production


class Grammar:
    def __init__(self, filename):
        self._non_terminals=[]
        self._terminals=[]
        self._starting_symbol=None
        self._productions= []
        self.read_from_file(filename)

    def getProdForNT(self, nonTerm):
        return list(
            filter(
                lambda x: x.getLeft() == nonTerm, self._productions)
        )

    def read_from_file(self, filename):
        with open(filename, 'r') as file:
            self.__nonTerminals = file.readline().strip().split(' ')
            self.__terminals = file.readline().strip().split(' ')
            self.__start = file.readline().strip()
            for line in file:
                production = line.strip().split(' ')
                key = production[0].strip()
                values = list(production[2].strip().split('|'))
                for value in values:
                    self._productions.append(
                        Production(key, value)
                    )
        file.close()



