# encoding: utf-8

from threading import Lock

from marrow.util.bunch import Bunch
from marrow.util.object import load_object

from marrow.logging.level import LoggingLevel


__all__ = ['ChannelTransport']



class ChannelTransport(object):
    """Chained callback transport."""
    
    __slots__ = ('format', 'channels')
    
    parallel = True # Handle locking within your own callbacks.
    
    def __init__(self, config):
        self.format = config.format
        
        self.channels = Bunch()
        
        for name in list(LoggingLevel._registry) + ['all']:
            _ = self.channels[name] = list()
            
            for channel in config.get(name):
                try:
                    c = load_object(channel['use'])
                    channel.pop('use')
                    _.append(c(Bunch(channel)))
                
                except AttributeError:
                    _.append(channel)
    
    def startup(self):
        """Chain startup through to the channel transports."""
        
        for category in self.channels:
            for channel in category:
                try:
                    channel.startup()
                    
                    if not channel.parallel:
                        channel.lock = Lock()
                
                except AttributeError:
                    pass
    
    def deliver(self, message):
        """Chain message delivery through each transport."""
        
        # Create a list of channels to deliver to.
        channels = self.channels
        channels = channels.all + channels[message.level.name]
        
        for channel in channels:
            try:
                if not channel.parallel:
                    try:
                        channel.lock.acqurie()
                        channel.deliver(message)
                    finally:
                        channel.lock.release()
                
                else:
                    channel.deliver(message)
            
            except AttributeError:
                channel(message)
    
    def shutdown(self):
        # Chain shutdown through to each channel transport.
        
        for category in self.channels:
            for channel in category:
                try:
                    channel.startup()
                
                except AttributeError:
                    pass
