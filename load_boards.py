# stores each board with key as board number and a 2d matrix of the respective sudoku board
# source of boards.txt: https://github.com/dimitri/sudoku/blob/master/sudoku.txt

boards = {}

with open("boards.txt", 'r') as f:
	for k in range(50):
		key = -1
		line = f.readline()
		sudoku_boards = []

		# handles case when grid number is between [1, 9]
		if line[-3] == '0':
			key = int(line[-2])
		else:
			key = int(line[-3:-1])

		for i in range(9):
			sudoku_board = []
			new_line = f.readline()

			for j in range(len(new_line)):
				# makes sure only numerical values are inserted in board, checking for newline
				char_ascii = ord(new_line[j])

				if char_ascii >= 48 and char_ascii <= 57:
					sudoku_board.append(int(new_line[j]))

			sudoku_boards.append(sudoku_board)

		boards[key] = sudoku_boards