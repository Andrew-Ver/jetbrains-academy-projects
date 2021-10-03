from typing import Tuple

class Tic_Tac_Toe():
	def __init__(self, grid_string : str = '_________'):
		self.row_one = [c for c in grid_string[0:3]]
		self.row_two = [c for c in grid_string[3:6]]
		self.row_three = [c for c in grid_string[6:]]
		self.list_repr = [[ch for ch in c] for c in [self.row_one, self.row_two, self.row_three]]
	
	def __repr__(self):
		# String Representation of the Grid to look like:
			#---------
			#| O _ O |
			#| X X O |
			#| _ X X |
			#---------
		return f"{'-'*9}\n| {' '.join(self.row_one)} |\n| {' '.join(self.row_two)} |\n| {' '.join(self.row_three)} |\n{'-'*9}"
	
	def current_state(self) -> str:
		# Current state of the board
		# Returns: 'Game not finished', 'Draw', 'X wins', 'O wins', or an 'Impossible' state
		def three_in_row(symbol : str) -> bool:
			# Check if there are 3 of symbol: str in a line horizontally, vertically or diagonally
			possible_three_in_row = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)], [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)], [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
			for pt in possible_three_in_row:
				if all([True if self.list_repr[X][Y] == symbol else False for X, Y in pt]):
					return True
			return False
		def full_grid() -> bool:
			# Are there any '_' spaces on the grid?
			return all([True if p in 'XO' else False for row in self.list_repr for p in row])
		def number_of_symb() -> tuple[int, int]:
			X_count = sum([1 for row in self.list_repr for p in row if p == 'X'])
			O_count = sum([1 for row in self.list_repr for p in row if p == 'O'])
			return (X_count, O_count)
		X_count, O_count = number_of_symb()
		if three_in_row('X') and not three_in_row('O'):
			return f'X wins'
		elif three_in_row('O') and not three_in_row('X'):
			return f'O wins'
		elif three_in_row('X') and three_in_row('O') or (X_count >= O_count+2) or (O_count >= X_count+2):
			return f'Impossible'
		elif not full_grid():
			return f'Game not finished'
		elif not three_in_row('X') and not three_in_row('O') and full_grid():	
			return f'Draw'
		else:
			return 'Impossible'

	def user_move_prompt(self, symbol: str) -> str:
		def make_move(row: int, col: int, symbol: str) -> str:
			if not (1 <= row <= 3) or not (1 <= col <= 3):
				print(f'Coordinates must be entered from 1 to 3!')
			elif self.list_repr[row-1][col-1] in 'XO':
				print(f'This cell is occupied! Choose a different one.')
			else:
				if row == 1:
					self.row_one[col-1] = symbol
				elif row == 2:
					self.row_two[col-1] = symbol
				elif row == 3:
					self.row_three[col-1] = symbol
				self.list_repr = [[ch for ch in c] for c in [self.row_one, self.row_two, self.row_three]]
				return f'OK'
		while True:
			print(f'{symbol} to move', end='\n')
			entry = input('Enter Coordinates:').split()
			if len(entry) == 2 and (entry[0].isnumeric() and entry[1].isnumeric()) and make_move(int(entry[0]), int(entry[1]), symbol) == 'OK':
				return f'OK'
			print(f'You should enter numbers!')


grid = Tic_Tac_Toe()
print(grid)

current_player = 'X'

while grid.current_state() not in ['Draw', 'X wins', 'O wins']:
	if grid.user_move_prompt(current_player) == 'OK':
		if current_player == 'X':
			current_player = 'O'
		else:
			current_player = 'X'
	print(grid)
print(grid.current_state())