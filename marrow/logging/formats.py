# encoding: utf-8


from marrow.util.bunch import Bunch

try:
    import simplejson as json

except ImportError:
    import json


__all__ = ['LineFormat', 'JsonFormat']



class DateTimeProxy(object):
    __slots__ = ('dt', )
    
    def __init__(self, dt):
        self.dt = dt
    
    def __getattr__(self, name):
        if name == 'iso':
            return self.dt.isoformat()
        
        return self.dt.strftime(name)



class LineFormat(object):
    def __init__(self, template="{now.iso}{s}{level.name}{s}{name}{data}{s}{text}",
            separator=' ', prefix='\n', newlines=True):
        self.defaults = Bunch(
                template = template,
                separator = separator,
                prefix = prefix,
                newlines = newlines
            )
    
    def __call__(self, message):
        options = Bunch(self.defaults)
        options.update(message.options)
        
        separator = options.separator
        
        data = Bunch(message.data)
        data.pop('now')
        data.pop('name')
        data.pop('level')
        data.pop('pid')
        data.pop('thread')
        data.pop('traceback')
        data = (separator + separator.join("{0}={1!r}".format(a, data[a]) for a in sorted(data))) if data else ""
        
        data_ = Bunch((i, message.data[i]) for i in ('name', 'level', 'pid', 'thread', 'traceback'))
        data_.now = DateTimeProxy(message.data.now)
        
        text = str(message)
        if not options.newlines:
            text = text.replace('\n', '\\n')
        
        if 'trace' in options:
            text += options.prefix + ((data_.traceback if options.prefix == '\n' else \
                    data_.traceback.replace('\n', options.prefix))).strip()
        
        print options.template.format(s=separator, message=message, text=text, data=data, **data_)


class JsonFormat(object):
    def __init__(self, source=False, **options):
        self.source = source
        self.options = options
    
    def __call__(self, message):
        pass
