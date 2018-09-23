__all__ = ['ChatCommandMixin']


class ChatCommandMixin:
    def say(self, *args, sep=' '):
        self.run('say', sep.join(map(str, args)))
