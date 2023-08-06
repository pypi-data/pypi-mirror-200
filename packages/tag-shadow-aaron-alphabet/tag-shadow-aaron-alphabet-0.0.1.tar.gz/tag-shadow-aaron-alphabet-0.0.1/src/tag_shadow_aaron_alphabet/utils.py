import os as _os 
import tomllib as _tomllib
import tomli_w as _tomli_w
import shutil as _shutil

def shadowfile(file):
	directory, filename = _os.path.split(file)
	if filename.startswith('.') or filename.endswith(".tag"):
		raise ValueError()
	filename = f".{filename}.tag"
	return _os.path.join(directory, filename)

def read_shadow(file):
	_file = shadowfile(file)
	if not _os.path.exists(_file):
		return dict()
	with open(_file, mode="rb") as fp:
    	data = tomllib.load(fp)
    for k, v in data.items():
    	if type(v) not in (bool, int, str, float):
    		raise TypeError()
    return data

def write_shadow(file, data):
    for k, v in data.items():
    	if type(v) not in (bool, int, str, float):
    		raise TypeError()
	with open(shadowfile(file), mode="wb") as fp:
		_tomli_w.dump(data, fp)

def tag_file(file, *tags):
	data = read_shadow(file)
	for tag in tags:
		data[tag] = True
	write_shadow(file, data)

def untag_file(file, *tags):
	data = read_shadow(file)
	for tag in tags:
		data.pop(tag, None)
	write_shadow(file, data)

def walk(*targets):
	for target in targets:
		if _os.path.isfile(target):
			yield target
			continue
		for (root, dirnames, filenames) in _os.walk(target):
			for filename in filenames:
				yield _os.path.join(root, filename)

