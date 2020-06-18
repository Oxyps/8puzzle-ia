from numpy import array, array_equal, where

class State:
	def __init__(self, matrix, level, fvalue, parent):
		self.matrix = array(matrix)
		self.level = level
		self.fvalue = fvalue
		self.parent = parent

	def __str__(self):
		return str(self.matrix)

	def __eq__(self, state):
		if state.fvalue != self.fvalue:
			return False

		return array_equal(self.matrix, state.matrix)
	
	def __ne__(self, state):
		return not array_equal(self.matrix, state.matrix)

	def __hash__(self):
		return hash(tuple(row) for row in self.matrix) * hash(self.fvalue) * hash(self.level)

	def already_exists(self, states_list):
		""" Check if the all state is in given list of states """

		return self in states_list

	def find_blank(self):
		""" Returns the position of the blank space """

		return where(self.matrix == 0)

	def move(self, x1, y1, x2, y2):
		""" Move the blank (x1, y1) to the given direction (x2, y2)\n
		if the given direction its out of limits return None """

		if x2 >= 0 and x2 < 3 and y2 >= 0 and y2 < 3:
			temp_matrix = self.matrix.copy()

			temp = temp_matrix[x2, y2]

			temp_matrix[x2, y2] = 0
			temp_matrix[x1, y1] = temp

			return temp_matrix

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
				child_state = State(child_matrix, self.level + 1, 0, None)
				children.append(child_state)

		return children