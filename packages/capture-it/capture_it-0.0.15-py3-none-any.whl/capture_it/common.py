



# -----------------------------------------------------------------------------

def juniper_add_no_more(cmd):
	"""returns updated juniper command with proper full | no-more statement if missing or trunkated found.

	Args:
		cmd (str): juniper show command

	Returns:
		str: updated command with | no-more
	"""	
	spl = cmd.split("|")
	no_more_found = False
	for i, item in enumerate(spl):
		if i == 0: continue
		no_more_found = item.strip().startswith("n")
		if no_more_found:
			spl[i] = " no-more "
			break
	if not no_more_found:
		spl.append( " no-more ")
	ucmd = "|".join(spl)
	return ucmd

