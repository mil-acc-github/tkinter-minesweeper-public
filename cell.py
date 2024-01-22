from tkinter import Button


class State:
	Covered   = "#F3B95F"
	Uncovered = "#6895D2"
	Flagged   = "#D04848"
	QMarked   = "#FDE767"

	@classmethod
	def strf(cls, state):
		return {
			cls.Covered  : "Covered"  ,
			cls.Uncovered: "Uncovered",
			cls.Flagged  : "Flagged"  ,
			cls.QMarked  : "QMarked"  ,
		}[state]

	@classmethod
	def UIstrf(cls, state, content="💣"):
		return {
			cls.Covered  : "",
			cls.Uncovered: str(content),
			cls.Flagged  : "🚩",
			cls.QMarked  : "❓",
		}[state]


class Number:
	def __init__(self, bomb_around):
		self.bomb_around = bomb_around

	def info(self):
		return str(self.bomb_around) if self.bomb_around != 0 else ""


class Content:
	Init = -99
	Bomb = "💣"
	Num  = Number


class Cell(Button):

	def init(self, board, pos):
		self.board = board
		self.game_lose:callable = board.game.lose

		self.pos = pos
		self.state = State.Covered
		self.content = Content.Init

		self.update()
		return self

	def init_post_01(self, is_bomb):
		self.content = Content.Bomb if is_bomb else Content.Num(0)

	def init_post_02(self, bomb_around):
		self.content = Content.Num(bomb_around=bomb_around)
		
	def is_bomb(self):
		return self.content == Content.Bomb

	def is_zero(self):
		if isinstance(self.content, Content.Num):
			return self.content.bomb_around == 0
		return False

	def is_open(self):
		return self.state == State.Uncovered

	def is_correct(self):
		if not self.is_bomb():
			return self.state == State.Uncovered
		return True

	def uncover_by_board(self):
		self.state = State.Uncovered
		self.update()

	def update(self):
		content = self.content
		if content == Content.Init:
			content = Content.Num(-1)
		if self.is_bomb() and self.is_open():
			self.configure(bg=State.Flagged)
		else:
			self.configure(bg=self.state)
		self.configure(
			text=State.UIstrf(
				state=self.state,
				content=content if (content == Content.Bomb) else content.info(),
			), 
			font=("MINE-SWEEPER", 12)
		)

	def clicked_L(self, _event):
		if self.content == Content.Init:
			self.board.first_click_on(self)
			self.state = State.Uncovered
		else:
			if self.state != State.Flagged:
				self.board.click_on(self)
				self.state = State.Uncovered
				if self.is_bomb():
					self.game_lose()

		self.update()

	def clicked_R(self, _event):
		if self.state == State.Covered:
			self.state = State.Flagged

		elif self.state == State.Flagged:
			self.state = State.QMarked

		elif self.state == State.QMarked:
			self.state = State.Covered

		self.update()


	def __repr__(self):
		return f"Cell(pos={self.pos}, state={State.strf(self.state)})"
