import copy

'''
    https://github.com/Balazshazialex/FLCD_Lab1
    Class SymbolTable - defined as a "hashmap", structured as a list of lists.
    HashFunction  is calculated by summing up the ASCII codes of each char from the string and returning the remainder to the number of small lists in self._map(in  this case chosen as 30)
    Function add will check if a string is in the table already and will return its position if found, otherwise will add it where deeemed fit and return the insert position

'''


class SymbolTable:
    def __init__(self):
        self._map = []
        for i in range(30):
            self._map.append(copy.deepcopy([]))

    def add(self, string):
        check_string = self.get_remainder(string)
        small_list = self._map[check_string]
        for i in range(len(small_list)):
            if small_list[i] == string:
                return (check_string, i)
        self._map[check_string].append(string)
        insert_position = (check_string, len(self._map[check_string]) - 1)
        return insert_position

    def get_remainder(self, string):
        sum = 0
        for char in string:
            sum += ord(char)
        return sum % 30

    '''
    pos is a tuple=(position_of_list,position_in_list)
    '''

    def get_string_from_pos(self, pos):
        return self._map[pos[0]][pos[1]]

    def __str__(self):
        string_builder = ""
        for elem in self._map:
            for i in elem:
                string_builder += i + "->" + str(self.add(i)) + '\n'
        return string_builder

#
# s = SymbolTable()
# s.add("a")
# s.add("b")
# print(s)
# print(s.add("a"))
# print(s.get_string_from_pos((7,0)))