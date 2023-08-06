import os as _os 
import tomllib as _tomllib
import tomli_w as _tomli_w
import shutil as _shutil
import string as _string

_tagchars = _string.ascii_lowercase + _string.digits + '_'

def tag(value):
	value = str(value).lower()
	ans = ""
	for x in value:
		if x in _tagchars:
			ans += x
		else:
			ans += '_'
	ans = ans.lstrip('_')
	if len(set(ans) - set(_string.digits)):
		return ans
	else:
		raise ValueError()


def shadowfile(file):
    directory, filename = _os.path.split(file)
    if filename.startswith('.') or filename.endswith(".tag"):
        raise ValueError()
    filename = f".{filename}.tag"
    return _os.path.join(directory, filename)

def check_shadowdata(data):
    for k, v in data.items():
        if tag(k) != k:
            raise ValueError()
        if type(v) not in (bool, int, str, float):
            raise TypeError()

def read_shadow(file):
    _file = shadowfile(file)
    if not _os.path.exists(_file):
        return dict()
    with open(_file, mode="rb") as fp:
        data = _tomllib.load(fp)
    check_shadowdata(data)
    return data

def write_shadow(file, data):
    check_shadowdata(data)
    with open(shadowfile(file), mode="wb") as fp:
        _tomli_w.dump(data, fp)

def tag_file(file, *tags):
    data = read_shadow(file)
    for k in tags:
        data[tag(k)] = True
    write_shadow(file, data)

def untag_file(file, *tags):
    data = read_shadow(file)
    for t in tags:
        data.pop(tag(t), None)
    write_shadow(file, data)

def walk(*targets):
    ans = list()
    for target in targets:
        if _os.path.isfile(target):
            if target not in ans:
                ans.append(target)
            continue
        for (root, dirnames, filenames) in _os.walk(target):
            for filename in filenames:
                if not (filename.startswith('.') or filename.endswith(".tag")):
                    file = _os.path.join(root, filename)
                    if file not in ans:
                        ans.append(file)
    return ans

def move(src, dst, force=False):
    if _os.path.isdir(src):
        return _shutil.move(src, dst)
    if _os.path.exists(dst):
        if not force:
            raise IOError()
    _shutil.move(src, dst)
    _src = name(src)
    _dst = name(dst)
    if _os.path.exists(_src):
        _shutil.move(_src, _dst)

def copy(src, dst, force=False):
    if _os.path.isdir(src):
        return _shutil.copytree(src, dst)
    if _os.path.exists(dst):
        if not force:
            raise FileExistsError()
    ans = _shutil.copy2(src, dst)
    _src = name(src)
    _dst = name(dst)
    if _os.path.exists(_src):
        _shutil.copy2(_src, _dst)
    return ans

def init(file):
    _file = shadowfile(file)
    if not _os.path.isfile(_file):
        write_shadow(file=file, data={})




