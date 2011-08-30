# encoding: utf-8

import os


__all__ = ['StreamTransport']



class FileTransport(object):
    """File-based logger."""
    
    __slots__ = ('lock', 'name', 'format', 'mode', 'buffer', 'file')
    
    parallel = False # Note the additional 'lock' slot, above.
    
    def __init__(self, config):
        self.name = config.name
        self.format = config.format
        self.mode = config.get('mode', 'a')
        self.buffer = config.get('buffer', True)
        self.file = None
    
    def startup(self):
        self.file = open(self.name, self.mode, self.buffering)
    
    def deliver(self, message):
        self.file.write(self.format(message))
    
    def shutdown(self):
        if self.file:
            self.file.close()
        
        self.file = None
