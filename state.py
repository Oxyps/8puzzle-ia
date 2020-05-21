from numpy import array_equal

class State:
    def __init__(self, matrix, level, fvalue):
        self.matrix = matrix
        self.level = level
        self.fvalue = fvalue

    def __str__(self):
        return str(self.matrix)

    def __eq__(self, state):
        if array_equal(self.matrix, state.matrix):
            return True
        return False

    def already_exists(self, states_list):
        for state in states_list:
            if self.__eq__(state):
                return True
        return False

    def copy(self):
        temp_matrix = []
        
        for line in self.matrix:
            temp = []
            
            for column in line:
                temp.append(column)
            
            temp_matrix.append(temp)

        return temp_matrix

    def find_blank(self):
        """ Returns the position of the blank space """

        for i in range(0, len(self.matrix)):
            for j in range(0, len(self.matrix)):
                if self.matrix[i][j] == ' ':
                    return i, j
    
    def move(self, x1, y1, x2, y2):
        """ Move the blank (x1, y1) to the given direction (x2, y2)\n
        if the given direction its out of limits return None """
        
        if x2 >= 0 and x2 < len(self.matrix) and y2 >= 0 and y2 < len(self.matrix):
            temp_matrix = self.copy()

            temp = temp_matrix[x2][y2]

            temp_matrix[x2][y2] = ' '
            temp_matrix[x1][y1] = temp
            
            return temp_matrix
        else:
            return None

    def generate_children(self):
        """ To generate child states from the given one by moving
        the blank space either in all directions """

        x, y = self.find_blank()

        directions = [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]
        children = []

        for direction in directions:
            child_matrix = self.move(x, y, direction[0], direction[1])

            if child_matrix is not None:
                child_state = State(child_matrix, self.level + 1, 0)
                children.append(child_state)
        
        return children