from . import utils

def tag(*, t, tags):
	files = utils.walk(t)
	for file in files:
		utils.tag_file(tags=tags, file=file)

def untag(*, t, tags):
	files = utils.walk(t)
	for file in files:
		utils.untag_file(tags=tags, file=file)

