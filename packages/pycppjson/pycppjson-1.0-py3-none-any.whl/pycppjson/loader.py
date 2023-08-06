import cppyy

from typing import Callable

CallableCFunc = Callable

def _include(): cppyy.include('loader.cxx')

def loads(to_loads:str="{}", loader:CallableCFunc=None, execs:Callable=eval):
	_include()
	loader = cppyy.gbl.load if loader is None else loader
	return execs(loader(to_loads))