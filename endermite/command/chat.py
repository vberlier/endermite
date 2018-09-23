__all__ = ['ChatCommandMixin']

import json


class ChatCommandMixin:
    def say(self, *args, sep=' '):
        self.run('say', sep.join(map(str, args)))

    def log(self, *args, sep=' ', color='gray', prefix='[LOG]'):
        self.run('tellraw', '@a', json.dumps({
            'text': prefix + ' ' + sep.join(map(str, args)),
            'color': color
        }))

    def error(self, *args, sep=' '):
        self.log(*args, sep, color='red', prefix='[ERR]')
