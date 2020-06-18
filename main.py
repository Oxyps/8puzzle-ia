from random import choice
from state import State

def path():
	path = []

	current_state = FINAL_STATE
	while current_state.parent:
		path.insert(0, current_state)
		current_state = current_state.parent
	path.insert(0, INITIAL_STATE)
	
	return path

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
	
	print('ESTADO OBJETIVO:')
	show(GOAL_STATE)

	print(f'NÚMERO DE ESTADOS FECHADOS: {len(closed_states)}')
	print(f'NÚMERO DE ESTADOS EM ABERTO: {len(opened_states)}')

	print(f'NÚMERO DE PASSOS ATÉ O OBJETIVO: {len(path())}\n\nCAMINHO ENCONTRADO:')
	for state in path():
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
	for row in current_matrix:
		for item in row:
			current_array.append(item)

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

	return current_state.level + h1(current_state.matrix, goal_state.matrix)
	# return current_state.level + h2(current_state.matrix, goal_state.matrix)

def astar():
	while True:
		# remove from start of opened states cause its upward ordered, so the start is the min fvalue
		current_state = opened_states[0]
		del opened_states[0]

		# close current state
		closed_states.append(current_state)

		# if the heuristic cost between the current matrix to the goal matrix is 0
		# then the best path, for the a* search with this heuristic, was achieved
		if h1(current_state.matrix, GOAL_STATE.matrix) == 0:
			return current_state
		# if h2(current_state.matrix, GOAL_STATE.matrix) == 0:
		# 	return current_state

		# calculate fvalue to all child states from current state
		for child in current_state.generate_children():
			child.fvalue = f(child, GOAL_STATE)
			child.parent = current_state
			opened_states.append(child)

		# upward sort opened states by fvalue
		opened_states.sort(key=lambda state: state.fvalue)

def bfs():
	while not opened_states.__eq__([]):
		# remove from begin of opened states
		current_state = opened_states[0]
		del opened_states[0]

		# close current state
		closed_states.append(current_state)

		# if the current state equals final state matrix
		# then the best path for the bfs search was achieved
		if current_state.__eq__(GOAL_STATE):
			return current_state

		# open the child states from current state
		for child in current_state.generate_children():
			# if not child.already_exists(opened_states) or not child.already_exists(closed_states):
			if not (child.already_exists(opened_states) and child.already_exists(closed_states)):
				child.parent = current_state
				opened_states.append(child)

def dfs():
	while not opened_states.__eq__([]):
		# remove from end of opened states
		current_state = opened_states[-1]
		del opened_states[-1]

		# close current state
		closed_states.append(current_state)

		# if the current state equals final state matrix
		# then the best path for the dfs search was achieved
		if current_state.__eq__(GOAL_STATE):
			return current_state

		# open the child states from current state
		for child in current_state.generate_children():
			if not (child.already_exists(opened_states) and child.already_exists(closed_states)):
				child.parent = current_state
				opened_states.append(child)

def issolvable():
	# transform a matrix in array without the blank
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

	return State(matrix, 0, 0, None)

INITIAL_STATE = State([[2, 8, 3], [1, 6, 4], [7, 0, 5]], 0, 0, None)
""" estados iniciais aleatórios
INITIAL_STATE = None
while True:
	INITIAL_STATE = random_state()
	if issolvable():
		break
"""

GOAL_STATE = State([[1, 2, 3], [8, 0, 4], [7, 6, 5]], 0, 0, None)

INITIAL_STATE.fvalue = f(INITIAL_STATE, GOAL_STATE)

opened_states = [INITIAL_STATE]
closed_states = []

""" rodar uma busca por vez
FINAL_STATE = bfs()
FINAL_STATE = dfs()
"""
FINAL_STATE = astar()

show_path()