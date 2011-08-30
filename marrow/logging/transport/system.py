# encoding: utf-8

import syslog


__all__ = ['SyslogTransport']



class SyslogTransport(object):
    """Standard syslog transport."""
    
    __slots__ = ('format', 'identity', 'options', 'facility')
    
    parallel = True
    
    priorities = [LOG_DEBUG, LOG_INFO, LOG_NOTICE, LOG_WARNING, LOG_ERR, LOG_CRIT]
    
    def __init__(self, config):
        self.format = config.format
        self.identity = config.get('identity', None)
        self.options = config.get('options', 0)
        self.facility = config.get('facility', syslog.LOG_USER)
    
    def startup(self):
        syslog.openlog(self.identity, self.options, self.facility)
    
    def deliver(self, message):
        priority = self.priorities[min(message.level // 10, 5)]
        syslog.syslog(priority, self.format(message))
    
    def shutdown(self):
        syslog.closelog()
