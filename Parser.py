from grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self._grammar = grammar
        self.firstSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.followSet = {i: set() for i in self._grammar.getNonTerminals()}
        self._table = {}
        self.generateFirst()
        self.generateFollow()

    def Loop(self, initialSet, items, additionalSet):
        copySet = initialSet
        for i in range(len(items)):
            if items[i] in self._grammar.getNonTerminals():
                copySet = copySet.union(entry for entry in self.firstSet[items[i]] if entry != 'E')
                if 'E' in self.firstSet[items[i]]:
                    if i < len(items) - 1:
                        continue
                    copySet = copySet.union(additionalSet)
                    break
                else:
                    break
            else:
                copySet = copySet.union({items[i]})
                break
        return copySet

    def generateFirst(self):
        isSetChanged = False
        for production in self._grammar.getProductions():
            key = production.getLeft()
            value = production.getRight()
            v = list(value)
            copySet = self.firstSet[key]
            copySet = copySet.union(self.Loop(copySet, v, ['E']))

            if len(self.firstSet[key]) != len(copySet):
                self.firstSet[key] = copySet
                isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for production in self._grammar.getProductions():
                key = production.getLeft()
                value = production.getRight()
                v = list(value)
                copySet = self.firstSet[key]
                copySet = copySet.union(self.Loop(copySet, v, ['E']))

                if len(self.firstSet[key]) != len(copySet):
                    self.firstSet[key] = copySet
                    isSetChanged = True

    def generateFollow(self):
        self.followSet[self._grammar.getStartSymbol()].add('E')
        isSetChanged = False
        for production in self._grammar.getProductions():
            key = production.getLeft()
            value = production.getRight()
            v = list(value)
            for i in range(len(v)):
                if v[i] not in self._grammar.getNonTerminals():
                    continue
                copySet = self.followSet[v[i]]
                if i < len(v) - 1:
                    copySet = copySet.union(self.Loop(copySet, v[i + 1:], self.followSet[key]))
                else:
                    copySet = copySet.union(self.followSet[key])
                if len(self.followSet[v[i]]) != len(copySet):
                    self.followSet[v[i]] = copySet
                    isSetChanged = True

        while isSetChanged:
            isSetChanged = False
            for production in self._grammar.getProductions():
                key = production.getLeft()
                value = production.getRight()
                v = list(value)
                for i in range(len(v)):
                    if v[i] not in self._grammar.getNonTerminals():
                        continue
                    copySet = self.followSet[v[i]]
                    if i < len(v) - 1:
                        copySet = copySet.union(self.Loop(copySet, v[i + 1:], self.followSet[key]))
                    else:
                        copySet = copySet.union(self.followSet[key])
                    if len(self.followSet[v[i]]) != len(copySet):
                        self.followSet[v[i]] = copySet
                        isSetChanged = True

    def generateTable(self):
        nonterminals = self._grammar.getNonTerminals()
        terminals = self._grammar.getTerminals()
        for i in self._grammar.getProductions():
            key=i.getLeft()
            right=i.getRight()
            right_splitted=list(right)
            index=i.getNumber()
            rowSymbol=key
            for columnSymbol in terminals+["E"]:
                    pair=(rowSymbol,columnSymbol)
                    if right_splitted[0]==columnSymbol and columnSymbol!="E":
                        self._table[pair]=(right,index)
                    elif right_splitted[0] in nonterminals and columnSymbol in self.firstSet[right_splitted[0]]:
                        if pair not in self._table.keys():
                            self._table[pair]=(right,index)
                        else:
                            print(pair)
                            print("Grammar is not LL(1).")
                            return
                    else:
                        if right_splitted[0]=="E":
                            for b in self.followSet[rowSymbol]:
                                if b == 'E':
                                    b = '$'
                                self._table[(rowSymbol, b)] = (right,index)
                        else:
                            firsts = set()
                            for production in self._grammar.getProductions():
                                if production.getLeft()==rowSymbol:
                                    if production.getRight() in  nonterminals:
                                        firsts = firsts.union(self.firstSet[production.getRight()])
                                    if 'E' in firsts:
                                        for b in self.followSet[rowSymbol]:
                                            if b == 'E':
                                                b = '$'
                                            if (rowSymbol, b) not in self._table.keys():
                                                self._table[(rowSymbol, b)] = (right,index)
        for t in terminals:
            self._table[(t, t)] = ('pop', -1)

        # rule 3
        self._table[('$', '$')] = ('acc', -1)


g = Grammar("grammar1.txt")
p = Parser(g)
p.generateTable()
print(p._table)