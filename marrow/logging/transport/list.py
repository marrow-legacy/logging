# encoding: utf-8

import os


__all__ = ['ListTransport']



class ListTransport(object):
    """Default no-op transport."""
    
    __slots__ = ('messages', 'maximum', 'preserve')
    
    parallel = True
    
    def __init__(self, config):
        self.messages = config.get('list', [])
        self.maximum = config.get('maximum', None)
        self.preserve = config.get('preserve', True)
    
    def startup(self):
        del self.messages[:]
    
    def deliver(self, message):
        messages = self.messages
        messages.append(message)
        
        if self.maximum:
            del messages[:len(message) - self.maximum]
    
    def shutdown(self):
        if not self.preserve:
            del self.messages[:]
