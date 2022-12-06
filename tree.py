from row import Row


class ParserOutput:
    def __init__(self,filename):
        self.filename=filename
        self.rows= []
        self.curentIndex=1

    def addRow(self,information,parent,leftSibling):
        row=Row(self.curentIndex,information,parent,leftSibling)
        self.curentIndex+=1
        self.rows.append(row)
        return self.curentIndex-1

    def displayTable(self):
        print("Index, info, parent, leftsibling")
        for row in self.rows:
            print(str(row.index)+"   "+str(row.information)+"   "+str(row.parent)+"   "+str(row.leftsibling))

    def writeToFile(self):
        f=open(self.filename)
        f.write("Index, info, parent, leftsibling")
        for row in self.rows:
            f.write(str(row.index) + str(row.information) + str(row.parent) + str(row.leftsibling))
        f.close()