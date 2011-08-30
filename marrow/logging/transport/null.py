# encoding: utf-8

import os


__all__ = ['NullTransport']



class NullTransport(object):
    """Default no-op transport."""
    
    __slots__ = ()
    
    parallel = True
    
    def __init__(self, config):
        pass
    
    def startup(self):
        pass
    
    def deliver(self, message):
        pass
    
    def shutdown(self):
        pass
