from game import Game
from vec import Vec2

class App:
	def __init__(self, config):
		self.game = Game(self, config)

	def init(self):
		self.game.init()

	def run(self):
		self.game.play()


if __name__ == "__main__":
	app = App({
		'title': 'Python Tkinter MineSweeper',
		'life' : 3,
		'board': {
			# 'size': Vec2(5,5),
		},
	})
	app.init()
	app.run()
