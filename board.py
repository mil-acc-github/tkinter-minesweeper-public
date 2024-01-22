from tkinter import Button
from random import random

from vec import Vec2
from cell import Cell, Content

class Board:
	def __init__(self, game):
		self.game = game
		self.config = game.config.get('board', dict())

		self._inited = False

	def init(self):
		self._inited = True
		self.board_size = self.config.get('size' , Vec2(20,20))

		shape = self.config.get('shape', Vec2(2,1))
		padxy = self.config.get('padxy', Vec2(1,1))

		self._board = [
			[ Cell(self.game.window, text=f"{x},{y}", width=shape.x, height=shape.y).init( self, Vec2(x,y) )
			for y in range(self.board_size.x) ]
			for x in range(self.board_size.y)
		]

		for row in self._board:
			for cell in row:
				cell.grid(row=cell.pos.x, column=cell.pos.y, padx=padxy.x, pady=padxy.y)
				cell.bind("<Button-1>", cell.clicked_L)
				cell.bind("<Button-2>", cell.clicked_R)
				cell.bind("<Button-3>", cell.clicked_R)

	def first_click_on(self, first_cell:Cell):
		first_cell.init_post_01(is_bomb=False)

		for row in self._board:
			for cell in row:
				if cell.content != Content.Init:
					continue
				is_bomb = random() < self.game.config.get('bomb_rate', 0.15)
				cell.init_post_01(is_bomb=is_bomb)

		for row in self._board:
			for cell in row:
				if cell.content == Content.Bomb:
					continue
				bomb_around = 0
				for pos in self._available_around(cell.pos, self.board_size):
					if self._board[pos.x][pos.y].is_bomb():
						bomb_around += 1
				cell.init_post_02(bomb_around=bomb_around)

		self.click_on(first_cell)
		self.game.start_click()

	def click_on(self, cell:Cell):
		if cell.is_zero():
			for pos in self._available_around(cell.pos, self.board_size):
				around_cell = self._board[pos.x][pos.y]
				if not around_cell.is_open():
					around_cell.uncover_by_board()
					self.click_on(around_cell)

	def check(self):
		if self._inited and all(
			cell.is_correct()
			for row in self._board
			for cell in row
		):
			self.game.win()

	@staticmethod
	def _available_around(pos, size):
		def _genset(xs, ys):
			return set( Vec2(pos.x+x, pos.y+y) for y in ys for x in xs if (not ( x == 0 and y == 0 )) )

		_all = _genset( xs=(-1, 0, 1), ys=(-1, 0, 1) )
		_rms = set()

		if   pos.x == 0:
			_rms = _rms | _genset( xs=(-1, ), ys=(-1, 0, 1) )
		elif pos.x == (size.x-1):
			_rms = _rms | _genset( xs=( 1, ), ys=(-1, 0, 1) )

		if   pos.y == 0:
			_rms = _rms | _genset( xs=(-1, 0, 1), ys=(-1, ) )
		elif pos.y == (size.y-1):
			_rms = _rms | _genset( xs=(-1, 0, 1), ys=( 1, ) )

		return _all - _rms
