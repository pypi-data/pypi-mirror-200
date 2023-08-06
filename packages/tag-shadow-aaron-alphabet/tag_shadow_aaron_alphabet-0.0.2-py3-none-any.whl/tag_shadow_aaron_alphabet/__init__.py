import argparse as _argparse
from . import _tasking
from . import _conditions

parser = _argparse.ArgumentParser(
    fromfile_prefix_chars='@',
    allow_abbrev=False,
)
_subparsers = parser.add_subparsers(dest='task', required=True)
_subparser = _subparsers.add_parser('tag')
_subparser.add_argument('targets', nargs='*')
_subparser.add_argument('tag')
_subparser = _subparsers.add_parser('untag')
_subparser.add_argument('targets', nargs='*')
_subparser.add_argument('tag')
_subparser = _subparsers.add_parser('cat')
_subparser.add_argument('targets', nargs='*')
_subparser = _subparsers.add_parser('purge')
_subparser.add_argument('targets', nargs='*')
_subparser = _subparsers.add_parser('init')
_subparser.add_argument('targets', nargs='*')
_subparser = _subparsers.add_parser('cp')
_subparser.add_argument('src')
_subparser.add_argument('dst')
_subparser.add_argument('-f', '--force', default=False, action='store_true')
_subparser = _subparsers.add_parser('find')
_subparser.add_argument('targets', nargs='*')
_subparser.add_argument('-c', '--condition', dest='c', type=_conditions.get_condition_function)
_subparser.add_argument('-x', '--exec', dest='x', nargs='+', action='append')
#_mv_subparser = _subparsers.add_parser('mv')
#_mv_subparser.add_argument('src') 
#_mv_subparser.add_argument('dst')
#_mv_subparser.add_argument('-f', '--force', default=False, action='store_true') 
#_cp_subparser = _subparsers.add_parser('cp')
#_cp_subparser.add_argument('src') 
#_cp_subparser.add_argument('dst')
#_cp_subparser.add_argument('-f', '--force', default=False, action='store_true') 
#_touch_subparser = _subparsers.add_parser('touch')
#_touch_subparser.add_argument('file')
#_find_subparser = _subparsers.add_parser('find')
#_find_subparser.add_argument('condition', nargs='?', default="")
#_find_subparser.add_argument('-I', '--input', dest='I', nargs='+', default=['.'])
#_find_subparser.add_argument('-e', '--edit', dest='e')

def main(args=None):
    ns = parser.parse_args(args)
    kwargs = vars(ns)
    task = kwargs.pop('task')
    getattr(_tasking, task)(**kwargs)


