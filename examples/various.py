# encoding: utf-8

import sys

from marrow.logging import log, Log, INFO, WARNING

from marrow.util.bunch import Bunch


if '-q' in sys.argv:
    log = Log(level=INFO)

elif '-qq' in sys.argv:
    log = Log(level=WARNING)


log = log.name('example')


# normal stuff
log.debug("Debugging message.")
log.error("Error level message.")
log.info('{0} is having issues in {where}.', 'GothAlice', where='sector 27')

# renaming
baz = log.name('baz')
baz.debug('Diz!')

# newline handling
log.info('user\ninput\nannoys\nus')
log.options(newlines=False).info('we\ndeal')

# exception handling
try:
    1/0
except:
    log.exceptions('error', prefix="\n").warning('oh noes')
    # The above can be simplified to log.exceptions()...
    # As exceptions are off by default, calling this method
    # enables them by default.

# additional data
log.data(path="less traveled", roads=42).info('Going for a walk')

# log only fields as data -- no positional arguments
log.info(paths=42, dolphins='thankful')


# a spiffy WebCore 2 example:

from functools import wraps

def logged(fn):
    @wraps(fn)
    def inner(self, *args, **kw):
        log = self.log.data(controller=self.__class__.__name__, method=fn.__name__)
        
        log.data(args=args, kw=kw).debug()
        
        try:
            result = fn(self, *args, **kw)
        
        except:
            log.exceptions().error()
            raise
        
        log.data(result=result).debug()
    
    return inner


class BaseController(object):
    def __init__(self, context):
        self.ctx = context
        self.log = log.name('request').data(
                id = id(context.request),
                user = context.identity.name if context.identity else None
            )


class RootController(BaseController):
    @logged
    def index(self):
        self.log.info("Inside request.")
        return './templates/epic.html', dict(name="Epic page.")
    
    @logged
    def explode(self):
        1/0


RootController(Bunch(request="mock1", identity=None)).index()
RootController(Bunch(request="mock2", identity=Bunch(name='amcgregor'))).index()


try:
    ctx = Bunch(request="mock3", identity=Bunch(id='amcgregor'))
    RootController(ctx)

except:
    log.exceptions().data(controller=RootController.__name__, context=ctx).error()


root = RootController(Bunch(request="mock4", identity=None))

try:
    root.explode()

except:
    pass
