# encoding: utf-8

import sys

import traceback

from marrow.util.bunch import Bunch
from marrow.util.tuple import NamedTuple


__all__ = ['Message']


class Message(NamedTuple):
    __slots__ = ()
    _fields = ('template', 'data', 'args', 'kwargs', 'options')
    
    def __new__(cls, level, template=None, data=None, args=None, kwargs=None, options=None):
        if template is None:
            template = ""
        
        data = Bunch(data if data is not None else {})
        options = Bunch(options if options is not None else {})
        
        if args is None:
            args = []
        
        if kwargs is None:
            kwargs = {}
        
        data.level = level
        
        if 'trace' in options:
            trace = options.get('trace')
            
            if trace == 'error':
                tb = sys.exc_info()
                if tb[0] is not None:
                    data.traceback = traceback.format_exc()
            
            else:
                # We assume a 3-tuple.
                data.traceback = traceback.format_exception(*trace)
        
        return NamedTuple.__new__(cls, template, data, args, kwargs, options)
    
    def __str__(self):
        return self.template.format(*self.args, **self.kwargs)
