# encoding: utf-8

from __future__ import unicode_literals

import traceback

from marrow.util.bunch import Bunch
from marrow.util.tuple import NamedTuple


__all__ = ['Message']


class Message(NamedTuple):
    __slots__ = ()
    _fields = ('level', 'template', 'fields', 'args', 'kwargs', 'options')
    
    def __init__(self, level=None, template=None, fields=None, args=None, kwargs=None, options=None):
        if template is None:
            template = ""
        
        fields = Bunch(fields if fields is not None else {})
        options = Bunch(options if options is not None else {})
        
        if args is None:
            args = []
        
        if kwargs is None:
            kwargs = {}
        
        fields.level = level
        
        if 'trace' in options:
            trace = options.get('trace')
            
            if trace == 'error':
                tb = sys.exc_info()
                if tb[0] is not None:
                    fields.traceback = traceback.format_exc()
            
            else:
                # We assume a 3-tuple.
                fields.traceback = traceback.format_exception(*trace)
        
        super(Message, self).__init__(level, template, fields, args, kwargs, options)
    
    def __str__(self):
        return self.template.format(*self.args, **self.kwargs)
