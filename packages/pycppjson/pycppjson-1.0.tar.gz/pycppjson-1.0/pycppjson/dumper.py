import cppyy

from typing import Callable

CallableCFunc = Callable

def _include(): cppyy.include('dumper.cxx')

def dumps(to_dumps:dict={}, dumper:CallableCFunc=None):
	_include()
	dumper = cppyy.gbl.dumps if dumper is None else dumper
	return dumper(str(to_dumps))