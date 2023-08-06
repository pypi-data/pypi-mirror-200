import argparse as _argparse
from . import _tasking

parser = _argparse.ArgumentParser(
	fromfile_prefix_chars='@',
	allow_abbrev=False,
)
_subparsers = parser.add_subparsers(dest='task', required=True)
_tag_subparser = _subparsers.add_parser('tag')
_tag_subparser.add_argument('tags', nargs='+')
_tag_subparser.add_argument('-t', '--targets', dest='t', nargs='+')
_tag_subparser = _subparsers.add_parser('untag')
_tag_subparser.add_argument('tags', nargs='+')
_tag_subparser.add_argument('-t', '--targets', dest='t', nargs='+')
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


