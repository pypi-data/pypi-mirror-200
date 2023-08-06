class console:
	def pt(*text, end="", join="", flush=True):
		print(*text, end=end, sep=join, flush=flush)

	def ptln(*text, join="", flush=True):
		pt(*text, end="\n", join=join, flush=flush)

	def write(*text, end="", join="", flush=True):
		pt(*text, end=end, join=join, flush=flush)

	def writeln(*text, join="", flush=True):
		ptln(*text, join=join, flush=flush)

	def read(prompt):
		return input(prompt)

	