import pygame
import turtle
from load_boards import boards

pygame.init()

WIDTH, HEIGHT = 720, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
pygame.display.set_caption("Sudoku Solver")
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont("Georgia", 22, bold=True)

# Handles the game board
class Grid:	
	def __init__(self, rows, columns, width, height, boards):
		self.rows = rows
		self.columns = columns
		self.width = width
		self.height = height
		self.win = WIN
		self.boards = boards

	def draw_lines(self):
		"""
			Draws the lines for the board and for every three lines, it makes a darker line to signify each indiviual box
		"""
		line_step = self.width // 9
		x = 0

		# draws horizontal lines, giving thickness at increments of 3
		for i in range(9):
			line_thickness = 1 if i % 3 != 0 else 2
			pygame.draw.lines(self.win, BLACK, False, [(x, 0), (x, self.height)], line_thickness)
			x += line_step

		y = 0

		# draws horizontal lines, giving thickness at increments of 3
		for i in range(9):
			line_thickness = 1 if i % 3 != 0 else 2
			pygame.draw.lines(self.win, BLACK, False, [(0, y), (self.width, y)], line_thickness)
			y += line_step

	def fill_board(self):
		"""
			Fills the board with each value in self.board. This is repeatedly called when trying to solve the board to show the visualization of the program's
			backtracking algorithm to solve the board
		"""

		square_center_x = self.width // 9 // 2
		square_center_y = self.height // 9 // 2
		step = self.width // 9

		for board in self.boards:
			for num in board:
				if num != 0:
					num_text = FONT.render(str(num), 1, BLACK)

					x = square_center_x - 50
					y = square_center_y - 50

					# Draw new rectangle in case there was text already present in that specific spot in the board
					pygame.draw.rect(self.win, (255, 255, 255), pygame.Rect(x, y, self.width // 9, self.height // 9))
					# As a result of previous call, lines go away so redrawing every time helps keep lines
					self.draw_lines()
					WIN.blit(num_text, (square_center_x - num_text.get_width(), square_center_y - num_text.get_height()))

				square_center_x += step

			square_center_x = self.width // 9 // 2
			square_center_y += step
		

	def is_valid(self, row, col, val):
		"""
			Checks if val can fit in the board as per Sudoku rules.
			In order for val to be considered valid it must follow these preconditions:
				- There must be no duplicate number in the spot's respective row
				- There must be no duplicate number in the spot's respective column
				- There must be no duplicate number in the spot's respective box
		"""

		for i in range(9):
			if self.boards[i][col] == val or self.boards[row][i] == val or self.boards[(row // 3) * 3 + i // 3][(col // 3) * 3 + i % 3] == val:
				return False
		return True

	def solve(self):
		"""
			Solves the board using a backtracking algorithm. Tries every number from [1, 10) and sees if it is valid as described in is_valid.
			If not, it tries other numbers, otherwise moves on to the next spot in the board. Keeps going until the entire board is solved.
		"""

		for row in range(len(self.boards)):
			for columns in range(len(self.boards[row])):
				pygame.event.pump()
				if self.boards[row][columns] == 0:
					for i in range(1, 10):
						if self.is_valid(row, columns, i):
							self.boards[row][columns] = i
							self.fill_board()

							# delays and updates board to show progress of algorithm
							pygame.time.delay(50)
							pygame.display.update()
							
							if self.solve():
								return True
							else:
								self.boards[row][columns] = 0
				
					return False

		# final display update to show finished product in a clean manner
		pygame.display.update()
		return True

def main():
	screen = turtle.Screen()
	screen.setup(0, 0)

	# used turtle to handle input and loading board from board.txt
	board_number = turtle.textinput("Load Board", "Choose a number from 1-50:")

	while board_number == None or not board_number.isdigit():
		board_number = turtle.textinput("Load Board", "Choose a number from 1-50:")

	screen.bye()

	# makes pygame window visible only after input is received
	global WIN
	WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SHOWN)

	clock = pygame.time.Clock()
	run = True

	game_grid = Grid(9, 9, WIDTH, HEIGHT, boards[int(board_number)])

	while run:
		clock.tick(60)
		WIN.fill((255, 255, 255))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		game_grid.draw_lines()
		game_grid.fill_board()
		game_grid.solve()

	pygame.quit()

if __name__ == "__main__":
	main()