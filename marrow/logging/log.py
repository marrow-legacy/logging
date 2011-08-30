# encoding: utf-8

import os
import datetime
import threading

from functools import partial

from marrow.util.bunch import Bunch
from marrow.util.tuple import NamedTuple

from marrow.logging.level import LoggingLevel
from marrow.logging.formats import LineFormat
from marrow.logging.message import Message


__all__ = ['Log']



class Log(NamedTuple):
    __slots__ = ()
    _fields = ('_data', '_options', 'level')
    
    def __new__(cls, data=None, options=None, level=None):
        data = Bunch(data) if data is not None else Bunch(name=None)
        options = Bunch(options) if options is not None else Bunch()
        level = level if level is not None else LoggingLevel._registry['debug']
        
        return NamedTuple.__new__(cls, data, options, level)
    
    def __getattr__(self, name):
        try:
            return super(Log, self).__getattr__(name)
        
        except AttributeError:
            pass
        
        if name not in LoggingLevel._registry:
            raise AttributeError("type object '{0}' has no attribute '{1}'".format(type(self).__name__, name))
        
        return partial(self.emit, LoggingLevel._registry[name])
    
    def name(self, replace=None, append=None):
        if replace and append:
            raise TypeError("Can not replace and append at the same time.")
        
        if append:
            return self.data(name=(self.data.get('name', '') + '.' + append).lstrip('.'))
        
        return self.data(name=replace)
    
    def data(self, **kw):
        log = Log(*self)
        log._data.update(kw)
        
        return log
    
    def options(self, **kw):
        log = Log(*self)
        log._options.update(kw)
        
        return log
    
    def trace(self, trace="error", prefix=None):
        if prefix:
            self = self.options(prefix=prefix)
        
        return self.options(trace=trace)
    
    def emit(self, level, template=None, *args, **kw):
        try:
            level.name
        except AttributeError:
            level = LoggingLevel._registry[level]
        
        if level < self.level:
            return
        
        if not template and args:
            raise TypeError("Positional arguments may only be used if a template is specified.")
        
        # Step one, find the appropriate formatter.
        
        # Step two, eliminate if the formatter level is greater than ours.
        
        # Step three, construct the message.
        
        data = Bunch(
                now = datetime.datetime.now(),
                thread = threading.currentThread().getName(),
                pid = os.getpid(),
                traceback = None
            )
        data.update(self._data)
        
        if not template:
            data.update(kw)
            kw.clear()
        
        message = Message(level, template, data, args, kw, self._options)
        
        # Step four, deliver.
        LineFormat()(message)
