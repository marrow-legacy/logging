# encoding: utf-8

from marrow.logging.message import Message
from marrow.logging.level import *
from marrow.logging.log import Log


__all__ = ['Log', 'Message'] + level.__all__ + ['log']


log = Log(data={'name': '-'})



"""

log.debug("Foo!")
log.error("Bar!")
log.info('{0} is having issues in {where}.', 'GothAlice', where='sector 27')

baz = log.name('baz')
baz.debug('Diz!')

log.info('user\ninput\nannoys\nus')
log.options(newlines=True).info('we\ndeal')

try:
    1/0
except:
    log.trace('error', prefix="\n").warning('oh noes')

log.data(path="less traveled", roads=42).info('Going for a walk')

# Log only fields -- no positional arguments.
log.info(paths=42, dolphins='thankful')

"""