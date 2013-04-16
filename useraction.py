INVALID = -1
EXIT = 0
MOVE = 1
SAVE = 2
ROQUE = 3
GROQUE = 4
HELP = 5

class UserAction:
	def __init__(self, action, data={}):
		self.action = action
		self.data = data