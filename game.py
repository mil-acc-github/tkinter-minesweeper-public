import tkinter as tk
from time import perf_counter

from vec import Vec2
from board import Board


class Game:
	def __init__(self, app, config):
		self.app = app
		self.config = config

		self.board = Board(self)

	def init(self):
		self.running = False
		self.life = self.config.get('life', '3')

		self.window = tk.Tk()
		self.window.title( self.config.get('title', 'Game') )
		self.window.geometry( self._make_geometry( self.config.get('window_size', Vec2(1280,820)) ) )
		self.window.resizable(False, False)

		self.board.init()

	def play(self):
		self.running = True
		self.window.mainloop()

	@staticmethod
	def _make_geometry(vec:Vec2):
		return f"{vec.x}x{vec.y}+{int(vec.x*0.2)}+100"

	def _retry(self, _event):
		self.window.destroy()
		self.init()
		self.play()

	def _game_end(self, text):
		self.running = False
		self.board._inited = False

		board_size = self.config.get('board_size', Vec2(960,820))

		lose_label = tk.Label(self.window, text=text, bg="black", fg="yellow", width=16, height=2, font=("MINE-SWEEPER", 24))
		lose_label.place(x=int(board_size.x*0.20), y=int(board_size.y*0.05))

		retry_btn = tk.Button(self.window, text="Retry?", bg="black", fg="yellow", width=12, height=1, font=("MINE-SWEEPER", 18))
		retry_btn.place(x=int(board_size.x*0.28), y=int(board_size.y*0.25))

		retry_btn.bind("<Button-1>", self._retry)

	def lose(self):
		self.life -= 1
		if self.life <= 0:
			self._game_end("You Lost...")

	def win(self):
		self._game_end("You Won!")

	def start_click(self):
		self.t0 = perf_counter()
		self.window.after(100, self.timer)

	def timer(self):
		board_size  = self.config.get('board_size', Vec2(960,820))

		time_passed = perf_counter() - self.t0

		(
			tk.Label(self.window, text="Time:", bg="#F0F0F0", fg="black", width=4, height=1, font=("MINE-SWEEPER", 12))
			.place(x=board_size.x+20, y=20)
		)
		(
			tk.Label(self.window, text=f"{time_passed:.0f}", bg="#F0F0F0", fg="black", width=6, height=1, font=("MINE-SWEEPER", 12))
			.place(x=board_size.x+168, y=20)
		)
		(
			tk.Label(self.window, text="Life:", bg="#F0F0F0", fg="black", width=4, height=1, font=("MINE-SWEEPER", 14))
			.place(x=board_size.x+20, y=80)
		)
		(
			tk.Label(self.window, text=f"{self.life}", bg="#F0F0F0", fg="black", width=6, height=1, font=("MINE-SWEEPER", 14))
			.place(x=board_size.x+160, y=80)
		)

		if self.running:
			self.board.check()
			self.window.after(400, self.timer)

	def stop(self):
		self.window.destroy()
