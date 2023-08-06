import os as _os 
import tomllib as _tomllib
import tomli_w as _tomli_w
import shutil as _shutil
import subprocess
import sys

from . import utils


    


def _file_decorator(oldfunc):
    def newfunc(*, targets, **kwargs):
        if len(targets) == 0:
            targets = ['.']
        files = utils.walk(*targets)
        for file in files:
            oldfunc(file=file, **kwargs)
    return newfunc

def cp(*, src, dst):
    utils.copy(src, dst)

def mv(*, src, dst):
    utils.move(src)

@_file_decorator
def cat(*, file):
    with open(utils.shadowfile(file), "r") as fp:
        print(fp.read(), end="")

@_file_decorator
def tag(*, file, tag):
    utils.tag_file(file, tag)

@_file_decorator
def untag(*, file, tag):
    utils.untag_file(file, tag)

@_file_decorator
def find(file, c, x):
    if not c(utils.read_shadow(file)):
        return
    if x is None:
        print(file)
    else:
        for line in x:
            cline = list()
            for v in line:
                if v == "-":
                    cline.append(file)
                else:
                    cline.append(v)
            subprocess.run(cline, check=True, stdout=sys.stdout, stderr=sys.stderr)
    

@_file_decorator
def init(file):
    utils.init(file)

@_file_decorator
def purge(*, file):
    _file = utils.shadowfile(file)
    if _os.path.exists(_file):
        _os.unlink(_file)


