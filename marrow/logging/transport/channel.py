# encoding: utf-8

from threading import Lock

from marrow.util.bunch import Bunch

from marrow.logging.level import LoggingLevel


__all__ = ['ChannelTransport']



class ChannelTransport(object):
    """Chained callback transport."""
    
    #__slots__ = ('format', 'identity', 'options', 'facility')
    
    parallel = True # Handle locking within your own callbacks.
    
    def __init__(self, config):
        self.format = config.format
        
        self.channels = Bunch()
        
        for name in LoggingLevel._registry:
            self.channels[name] = list()
            # TODO: load up the channels from the config.
        
        self.channels.all = list()
        # TODO: As above.
    
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
