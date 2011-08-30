# encoding: utf-8

from functools import partial

from marrow.util.futures import ScalingPoolExecutor


__all__ = ['DynamicManager']

log = __import__('logging').getLogger(__name__)



class DynamicManager(object):
    __slots__ = ('workers', 'divisor', 'timeout', 'executor', 'transport')
    
    Executor = ScalingPoolExecutor
    
    def __init__(self, config, transport):
        self.workers = config.get('workers', 10) # Maximum number of threads to create.
        self.divisor = config.get('divisor', 10) # Estimate the number of required threads by dividing the queue size by this.
        self.timeout = config.get('timeout', 60) # Seconds before starvation.
        
        self.executor = None
        
        super(DynamicManager, self).__init__()
    
    def startup(self):
        log.info("%s manager starting up.", self.name)
        
        log.debug("Initializing transport queue.")
        self.transport.startup()
        
        workers = self.workers
        log.debug("Starting thread pool with %d workers." % (workers, ))
        self.executor = self.Executor(workers, self.divisor, self.timeout)
        
        log.info("%s manager ready.", self.name)
    
    def deliver(self, message):
        # Return the Future object so the application can register callbacks.
        # We pass the message so the executor can do what it needs to to make
        # the message thread-local.
        return self.executor.submit(partial(worker, self.transport), message)
    
    def shutdown(self, wait=True):
        log.info("%s manager stopping.", self.name)
        
        log.debug("Stopping thread pool.")
        self.executor.shutdown(wait=wait)
        
        log.debug("Draining transport queue.")
        self.transport.shutdown()
        
        log.info("%s manager stopped.", self.name)
