def pt(*text, end="", join="", flush=True):
	print(*text, end=end, sep=join, flush=flush)

def ptln(*text, join="", flush=True):
	pt(*text, end="\n", join=join, flush=flush)
