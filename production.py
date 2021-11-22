class Production:
    def __init__(self, leftSide, rightSide):
        self._leftSide = leftSide
        self._rightSide = rightSide

    def getLeft(self):
        return self._leftSide

    def getRight(self):
        return self._rightSide

    def __str__(self):
        rightStr = "["
        for i in range(len(self.getRight())):
            if i != len(self.getRight()) - 1:
                rightStr += self.getRight()[i]
            else:
                rightStr += self.getRight()[i]
        rightStr += "]"
        return self._leftSide + " -> " + rightStr

    def __eq__(self, other):
        return self._rightSide == other.getRight() and self._leftSide == other.getLeft()