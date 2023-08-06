
import os
import string
from . import utils



class Get:
    def __init__(self, key):
        self._key = utils.tag(key)
    def __call__(self, data):
        ans = data.get(self._key, False)
        return ans
class Operation:
    def __init__(self, *funcs):
        self._funcs = funcs
    def __call__(self, data):
        values = [func(data) for func in self._funcs]
        ans = type(self).run(*values)
        return ans
    def run(*args):
        raise NotImplementedError()
class Not(Operation):
    def run(arg):
        return not arg
class And(Operation):
    def run(*args):
        return all(args)
class Or(Operation):
    def run(*args):
        return any(args)
class Xor(Operation):
    def run(*args):
        return bool(sum(bool(arg) for arg in args) % 2)

def get_phrase_function(lines):
    while '~' in lines:
        i = lines.index('~')
        head = lines[:i]
        tail = lines[i+2:]
        lines = head + [Not(lines[i+1])] + tail
    while len(lines) > 1:
        a, op, b, *tail = lines
        func = {
            '^': Xor,
            '&': And,
            '|': Or,
        }[op]
        lines = [func(a, b)] + tail
    return lines[0]


def get_condition_function(phrase):
    phrase = str(phrase)
    lines = list()
    breaker = True
    for x in phrase:
        if x in string.whitespace:
            breaker = True
            continue
        if x in "()~&|^":
            lines.append(x)
            breaker = True
            continue
        if breaker:
            lines.append(x)
            breaker = False
            continue
        lines[-1] += x
    _lines = lines
    lines = list()
    for line in _lines:
        if line in "()~&|^":
            lines.append(line)
        else:
            lines.append(Get(line))
    while len(lines) > 1:
        try:
            closing = lines.index(')')
        except ValueError:
            return get_phrase_function(lines)
        opening = closing - 1
        while True:
            if lines[opening] == '(':
                break
            opening -= 1
            if opening < 0:
                raise ValueError()
        head = lines[:opening]
        body = lines[opening+1:closing]
        tail = lines[closing+1:]
        lines = head + [get_phrase_function(body)] + tail
    return lines[0]







