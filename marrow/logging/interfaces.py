# encoding: utf-8

from marrow.interface import Interface
from marrow.interface.schema import Method


__all__ = ['ITransport']


class IPlugin(Interface):
    startup = Method(args=0)
    deliver = Method(args=1)
    shutdown = Method(args=0)


class ITransport(IPlugin):
    __init__ = Method(args=1)
