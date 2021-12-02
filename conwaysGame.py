'''
Conways Game is a commandline based conways game of life.
This the thrid revision:
Plan:
	Step-one: Start with a command line based verion of conways game of life.
	+ This will require:
		-Ability to create, edit, save and load grids.
		-Ability to save and load a recorded set of frames

	Step-Two: Create a GUI
	+Must be simple
	+incude a play button

'''
import random
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

import threading

class Board:
	def __init__(self, columns:int = 10, rows:int = 10):
		self.columns:int = columns
		self.rows:int = rows
		self.grid:dict = self.new_grid(rand = True)

	# def flip_cell_state(self, pos):
	# 	if self.grid[pos]:
	# 		self.grid[pos] = False
	# 	else:
	# 		self.grid[pos] = True

	def count_alive(self, pos:tuple) -> int():
		# Returns the total cells that are alive around a givin point (x, y)
		x, y = pos
		neighbors = [(x + 1, y), # Right
					(x - 1, y), # Left
					(x + 1, y + 1), # Bottom Right
					(x - 1, y - 1), # Top Left
					(x + 1, y - 1), # Top Right
					(x - 1, y + 1), # Bottom Left
					(x, y + 1), # Bottom
					(x, y - 1)] # Top
		
		return sum(self.grid[(bor[0] % self.columns, bor[1] % self.rows)] for bor in neighbors)
		
	def quick_germ(self) -> dict():
		next_gen = {}
		for pos in self.grid:
			live_neighbors = self.count_alive(pos)
			if live_neighbors == 3:
				next_gen[pos] = True
			elif live_neighbors < 2 or live_neighbors > 3:
				next_gen[pos] = False
			else:
				next_gen[pos] = self.grid[pos]
		return next_gen

	def change_cell(self, pos):
		self.grid[pos] = not self.grid[pos]

	def step(self, times = 1):
		''' Goes through times generations'''
		for _ in range(times):
			next_grid = self.quick_germ()
			self.grid = next_grid

	def export_board(self):
		with open('saved_board.txt', 'w') as f:
			for k, v in self.grid.items():
				f.write(f'"{k}" = "{v}"')



	def clear_grid(self):
		self.grid = None
		self.grid = self.new_grid()

	def new_grid(self, rand:bool = False) -> dict():
		''' Returns a dict of grid	
			rand: If true will return a grid of random elements of True or False
		'''
		for col in range(self.columns):		
			if rand == False:
				return {(col, row): False for row in range(self.rows) for col in range(self.columns)}
			else:
				is_alive = random.choice
				return {(col, row): is_alive([True , False]) for row in range(self.rows) for col in range(self.columns)}

	def show_to_console(self):
		for x in range(self.columns):
			print()
			for y in range(self.rows):
				print(int(self.grid[(x, y)]), end = ' ')

	def living_cells(self) -> dict():
		''' return a dict of living cells to draw'''
		
		return {pos: state for pos, state in self.grid.items() if state == True}



class Window:
	def __init__(self, board: Board):
		self.root = tk.Tk()

		self.board = board

		self.playing = False

		self.pen_size = 5
		self.width = board.columns * self.pen_size
		self.height = board.rows * self.pen_size

		self.canvas_frame = tk.Frame(self.root)
		self.canvas_frame.pack(side='right')

		self.canvas = tk.Canvas(self.canvas_frame, width = self.width, height = self.height)
		self.canvas.pack(fill='both', expand = True)

		self.photo = Image.new('RGB', (self.width ,self.height))
		self.pen = ImageDraw.Draw(self.photo)
		self.image = ImageTk.PhotoImage(self.photo)
		self.draw()

		#Buttons and Bindings
		self.canvas.bind('<Button-1>', self.flip_cell)

		self.play_button = tk.Button(self.root, text = 'Play', command = self.play)
		self.stop_button = tk.Button(self.root, text = 'Stop', command = self.stop)
		self.clear_button = tk.Button(self.root, text = 'Clear', command = self.clear_board)
		self.save_button = tk.Button(self.root, text = 'Save', command = self.save)
		self.play_button.pack()
		self.stop_button.pack()
		self.clear_button.pack()
		self.save_button.pack()

	def clear_board(self):
		self.board.clear_grid()
		self.draw()

	def save(self):
		self.board.export_board()

	def play(self):
		self.playing = True
		self.flip()

	def stop(self):
		self.playing = False

	def flip(self):	
		if self.playing:
			self.board.step()
			self.draw()
			self.root.after(10, self.flip)

	def flip_cell(self, event):
		x = event.x//self.pen_size
		y = event.y//self.pen_size
		self.board.change_cell((x, y))
		self.draw()

	def clear(self):
		self.canvas.delete('all')
		self.pen.rectangle((0,0, self.width, self.height), fill='black')

	def draw(self):
		self.clear()
		for pos in self.board.living_cells():
			i = pos[0] * self.pen_size
			j = pos[1] * self.pen_size
			self.pen.rounded_rectangle(((i, j),(i + self.pen_size, j + self.pen_size)), radius = 1, fill = 'green')
	
		self.image = ImageTk.PhotoImage(self.photo)
		self.canvas.create_image(0, 0, image = self.image, anchor = 'nw')

	def run(self):
		''' Runs the mainloop'''
		self.root.mainloop()

class App:
	def __init__(self, columns, rows):
		self.game = Board(columns, rows)
		self.game_window = Window(self.game)

		self.game_window.run()

if __name__ == '__main__':

	game = App(100, 100)