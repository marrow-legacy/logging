# encoding: utf-8

from __future__ import unicode_literals

from marrow.util.tuple import NamedTuple


__all__ = ['LoggingLevel', 'DISABLED']



class LoggingLevel(NamedTuple):
    """This describes a logging level using a named tuple for efficiency and to allow sorting.
    
    Interesting note:
    Roughly 80 bytes of memory for each level (if the name is four characters long).
    """
    
    __slots__ = ()
    _fields = ('level', 'name')
    _registry = {}
    
    def __init__(self, *args, **kw):
        self._registry[self.name.lower()] = self
        super(LoggingLevel, self).__init__(*args, **kw)
    
    def __repr__(self):
        return 'LoggingLevel({0}, {1})'.format(self.level, self.name)
    
    def __int__(self):
        return self.level
    
    def __str__(self):
        return self.name


# Generate the default logging levels.
for level, name in enumerate(('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL')):
    locals()[name] = LoggingLevel(level * 10, name)
    __all__.append(name)

# Disabled is a special case as it must be above everything else.
DISABLED = LoggingLevel(99, 'DISABLED')

# Clean up.
del level, name
