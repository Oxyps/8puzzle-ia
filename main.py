from random import choice
from state import State

def show(state):
	for line in state.matrix:
		for value in line:
			if value == 0:
				print('  ', end='')
			else:
				print(f'{value} ', end='')
		print()
	print()

def show_path():
	print('ESTADO INICIAL:')
	show(INITIAL_STATE)
	
	print('\nESTADO OBJETIVO:')
	show(GOAL_STATE)

	print(f'\nNÚMERO DE PASSOS: {len(closed_states) - 1}\nCAMINHO ENCONTRADO:')
	for state in closed_states:
		show(state)

def h1(current_matrix, goal_matrix):
	""" This heuristic increments by 1 for each value that's out of goal position """

	heuristic = 0

	for current_line, goal_line in zip(current_matrix, goal_matrix):
		for current, goal in zip(current_line, goal_line):
			if current != goal and current != 0:
				heuristic += 1

	return heuristic

def h2(current_matrix, goal_matrix):
	""" This heuristic return the Manhattan distance for each tile out'o position """
	
	current_array = []
	goal_array = []

	for row1, row2 in zip(current_matrix, goal_matrix):
		for item1, item2 in zip(row1, row2):
			current_array.append(item1)
			goal_array.append(item2)

	heuristic = 0
	
	for i in range(3):
		for j in range(3):
			if goal_matrix[i][j] != 0:
				x, y = divmod(current_array.index(goal_matrix[i][j]), 3)
				heuristic += abs(x - i) + abs(y - j)

	return heuristic

def f(current_state, goal_state):
	""" Returns f(x) = g(x) + h(x)\n
		Where g(x) means the current state level in graph\n
		and the h(x) an heuristic cost to the current state to the goal state"""

	# return current_state.level + h1(current_state.matrix, goal_state.matrix)
	return current_state.level + h2(current_state.matrix, goal_state.matrix)

def random_state():
	choose = [1, 2, 3, 4, 5, 6, 7, 8, 0]

	matrix = []

	for i in range(3):
		line = []
		for j in range(3):
			chosen = choice(choose)
			line.append(chosen)
			choose.remove(chosen)
		matrix.append(line)

	return State(matrix, 0, 0)

def astar():
	while True:
		# remove from the start cause its upward ordered, so the start is the min fvalue
		current_state = opened_states[0]

		# close current state and delete from opened states list
		closed_states.append(current_state)
		del opened_states[0]

		# if the heuristic cost between the current matrix to the goal matrix is 0
		# then the best path, for the a* search with this heuristic, was achieved
		# if h1(current_state.matrix, GOAL_STATE.matrix) == 0:
		# 	break
		if h2(current_state.matrix, GOAL_STATE.matrix) == 0:
			break

		# calculate fvalue to all child states from current state
		for child in current_state.generate_children():
			child.fvalue = f(child, GOAL_STATE)
			opened_states.append(child)

		# upward sort opened states by fvalue
		opened_states.sort(key=lambda state: state.fvalue)

def dfs():
	while not opened_states.__eq__([]):
		# remove from the end
		current_state = opened_states[-1]

		# close current state and delete from opened states list
		closed_states.append(current_state)
		del opened_states[-1]

		# if the current state equals final state matrix
		# then the best path for the dfs search was achieved
		if current_state.__eq__(GOAL_STATE):
			break

		# open the child states from current state
		for child in current_state.generate_children():
			if not (child.already_exists(opened_states) and child.already_exists(closed_states)):
				opened_states.append(child)

def bfs():
	while not opened_states.__eq__([]):
		# remove from the beginning
		current_state = opened_states[0]

		# close current state and delete from opened states list
		closed_states.append(current_state)
		del opened_states[0]

		# if the current state equals final state matrix
		# then the best path for the bfs search was achieved
		if current_state.__eq__(GOAL_STATE):
			break

		# open the child states from current state
		for child in current_state.generate_children():
			if not (child.already_exists(opened_states) and child.already_exists(closed_states)):
				opened_states.append(child)

def issolvable():
	# transform a matrix in array
	array = []
	for line in INITIAL_STATE.matrix:
		for value in line:
			if value != 0:
				array.append(value)

	# count number of 'inversions'
	inversion_count = 0
	for i in range(0, len(array) - 1):
		for j in range(i + 1, len(array)):
			if array[i] > array[j]:
				inversion_count += 1

	# if the number of inversions is even then is solvable
	return inversion_count % 2 == 0

# INITIAL_STATE = State([[2, 8, 3], [1, 6, 4], [7, 0, 5]], 0, 0)
while True:
	INITIAL_STATE = random_state()
	if issolvable():
		break
	del INITIAL_STATE

GOAL_STATE = State([[1, 2, 3], [8, 0, 4], [7, 6, 5]], 0, 0)

INITIAL_STATE.fvalue = f(INITIAL_STATE, GOAL_STATE)

opened_states = [INITIAL_STATE]
closed_states = []

astar()

# dfs()
# bfs()

show_path()