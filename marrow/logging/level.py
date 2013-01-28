# encoding: utf-8

from __future__ import unicode_literals

import sys

from marrow.util.object import RichComparisonMixin


__all__ = ['LoggingLevel', 'DISABLED']


class LoggingLevel(RichComparisonMixin):
    """A sortable logging level."""

    __slots__ = ('level', 'name')
    _registry = {}

    def __init__(self, level, name):
        self.level = level
        self.name = name

        self._registry[self.name.lower()] = self
        super(LoggingLevel, self).__init__()

    def __repr__(self):
        return 'LoggingLevel({0}, {1})'.format(self.level, self.name)

    def __int__(self):
        return self.level
    
    def __unicode__(self):
        return self.name
    
    def __bytes__(self):
        return self.__unicode__.encode('ascii')
    
    if sys.version_info[0] == 2:
        __str__ = __bytes__
    else:
        __str__ = __unicode__

    def __eq__(self, other):
        return int(self) == int(other)

    def __lt__(self, other):
        return int(self) < int(other)


# Generate the default logging levels.
for level, name in enumerate(('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL')):
    locals()[name] = LoggingLevel(level * 10, name)
    __all__.append(name)

# Disabled is a special case as it must be above everything else.
DISABLED = LoggingLevel(99, 'DISABLED')

# Clean up.
del level, name
