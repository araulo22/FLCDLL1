from Splitter import Splitter
from grammar import Grammar
from tokenizer import Tokenizer
from tree import ParserOutput


class Parser:
    def __init__(self, grammar):
        self._grammar = grammar
        self.firstSet = {i: set() for i in self._grammar.getNonTerminals()}
        self.followSet = {i: set() for i in self._grammar.getNonTerminals()}
        self._table = {}
        self._parserOutput = ParserOutput("tree.txt")
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
            key = i.getLeft()
            right = i.getRight()
            right_splitted = list(right)
            index = i.getNumber()
            rowSymbol = key
            for columnSymbol in terminals + ["E"]:
                pair = (rowSymbol, columnSymbol)
                if right_splitted[0] == columnSymbol and columnSymbol != "E":
                    self._table[pair] = (right, index)
                elif right_splitted[0] in nonterminals and columnSymbol in self.firstSet[right_splitted[0]]:
                    if pair not in self._table.keys():
                        self._table[pair] = (right, index)
                    else:
                        print(pair)
                        print("Grammar is not LL(1).")
                        return
                else:
                    if right_splitted[0] == "E":
                        for b in self.followSet[rowSymbol]:
                            if b == 'E':
                                b = '$'
                            self._table[(rowSymbol, b)] = (right, index)
                    else:
                        firsts = set()
                        for production in self._grammar.getProductions():
                            if production.getLeft() == rowSymbol:
                                if production.getRight() in nonterminals:
                                    firsts = firsts.union(self.firstSet[production.getRight()])
                                if 'E' in firsts:
                                    for b in self.followSet[rowSymbol]:
                                        if b == 'E':
                                            b = '$'
                                        if (rowSymbol, b) not in self._table.keys():
                                            self._table[(rowSymbol, b)] = (right, index)
        for t in terminals:
            self._table[(t, t)] = ('pop', -1)
        self._table[('$', '$')] = ('acc', -1)

    def evaluateSequence(self, sequence):

        # w = list(sequence)
        w = sequence
        stack = [self._grammar.getStartSymbol(), '$']
        output = ""
        while stack[0] != '$' and w:
            print(w, stack)
            # pop operation
            if w[0] == stack[0]:
                w = w[1:]
                stack.pop(0)
            else:
                x = w[0]
                a = stack[0]
                # error operation
                if (a, x) not in self._table.keys():
                    return None
                # push operation
                else:
                    stack.pop(0)
                    rhs, index = self._table[(a, x)]
                    rhs = list(rhs)
                    for i in range(len(rhs) - 1, -1, -1):
                        if rhs[i] != 'E':
                            stack.insert(0, rhs[i])
                    output += str(index) + " "
            print(output)
        # error operation
        if stack[0] == '$' and w:
            return None
        # push operation or accept
        elif not w:
            if stack[0] == '$':
                print("accept")
            while stack[0] != '$':
                a = stack[0]
                if (a, '$') in self._table.keys():
                    output += str(self._table[(a, '$')][1]) + " "
                stack.pop(0)
                print(output)

            return output

    def constructParseTree(self, sequence):
        # add starting symbol and take its index
        new_sequence=[]
        for char in sequence:
            if char!=' ':
                new_sequence.append(char)
        idx = self._parserOutput.addRow(self._grammar.getStartSymbol(), 0, 0)
        sequenceIndex = 0
        self.addChildren(new_sequence, sequenceIndex, idx)
        self._parserOutput.displayTable()
        self._parserOutput.writeToFile()

    def addChildren(self, sequence, sequenceIndex, parentIndex):
        p = self._grammar.getProductionByIndex(sequence[sequenceIndex])
        sequenceIndex += 1
        nonTerminalsChildrenIndices = []
        prev = 0
        for child in list(p.getRight()):
            rowIndex = self._parserOutput.addRow(child, parentIndex, prev)
            if child in self._grammar.getNonTerminals():
                nonTerminalsChildrenIndices.append(rowIndex)
            prev = rowIndex
        childrenIdx = 0
        for child in list(p.getRight()):
            if child in self._grammar.getNonTerminals():
                self.addChildren(sequence, sequenceIndex, nonTerminalsChildrenIndices[childrenIdx])
                childrenIdx += 1


def pif_parser(infile):
    f = open(infile)
    lines = f.readlines()
    keywords = []
    for line in lines:
        keywords.append(line.split()[0])
    return keywords


g = Grammar("grammar1.txt")
ok = 0
p = Parser(g)
p.generateTable()
print(p.firstSet)
print(p.followSet)
print(p._table)
f = open('p2.txt', 'r')
text = f.read()
s = Splitter(text)
words = s.get_splitted()
t = Tokenizer(words)
seq = pif_parser("pif.txt")
output=p.evaluateSequence(["b", "b", "c", "a"])
p.constructParseTree(output)
