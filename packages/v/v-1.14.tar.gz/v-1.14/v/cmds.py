class Console:
	def __init__(self):
		self._bg = "0"
		self._fg = "0"
	def pt(self, *text, end="", join="", flush=True):
		print(*text, end=end, sep=join, flush=flush)

	def ptln(self, *text, join="", flush=True):
		pt(*text, end="\n", join=join, flush=flush)

	def write(self, *text, end="", join="", flush=True):
		pt(*text, end=end, join=join, flush=flush)

	def writeln(self, *text, join="", flush=True):
		ptln(*text, join=join, flush=flush)

	def read(self, prompt):
		return input(prompt)
	
	def set_bg(self, value):
		self._bg = value
		print(f"\u001b[{self._bg}m", end="")
	
	def get_bg(self):
		return self._bg

	bg = property(get_bg, set_bg)

	def set_fg(self, value):
		self._fg = value
		print(f"\u001b[{self._fg}m", end="")
	
	def get_fg(self):
		return self._fg

	bg = property(get_fg, set_fg)

console = Console()