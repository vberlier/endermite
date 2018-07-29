__all__ = ['CommandMixin']

from .function import FunctionBuilder


class ContextAwareMixin:
    def __init__(self, *args, context, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = context


class CommandMixin(ContextAwareMixin):
    """Expose context-modifying methods that mirror minecraft commands."""

    def _run(self, command_object):
        self.ctx[FunctionBuilder].register_command(command_object)

    def say(self, *args, sep=' '):
        self._run('say ' + sep.join(map(str, args)))  # TEMPORARY
