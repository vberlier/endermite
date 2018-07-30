__all__ = ['CommandMixin']

from .function import FunctionBuilder


class ContextAwareMixin:
    def __init__(self, *args, ctx, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx


class Command(tuple):
    """Hold the different parts of a minecraft command."""
    __slots__ = ()

    def __str__(self):
        return ' '.join(str(arg).replace('\n', ' ').strip() for arg in self)


class CommandMixin(ContextAwareMixin):
    """Expose context-modifying methods that mirror minecraft commands."""

    def run(self, *args):
        self.ctx[FunctionBuilder].register_command(Command(args))

    def say(self, *args, sep=' '):
        self.run('say', sep.join(map(str, args)))
