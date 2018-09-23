__all__ = ['BasicCommandMixin']

import json


class BasicCommandMixin:
    def say(self, *args, sep=' '):
        self.run('say', sep.join(map(str, args)))

    def log(self, *args, sep=' ', color='gray', prefix='[LOG]'):
        self.run('tellraw', '@a', json.dumps({
            'text': prefix + ' ' + sep.join(map(str, args)),
            'color': color
        }))

    def error(self, *args, sep=' '):
        self.log(*args, sep, color='red', prefix='[ERR]')

    def add_tag(self, tag):
        self.run('tag', '@s', 'add', tag)

    def remove_tag(self, tag):
        self.run('tag', '@s', 'remove', tag)
