__all__ = ['CommandMixin']

from contextlib import contextmanager

from ..function import FunctionBuilder
from .basic import BasicCommandMixin


class Command(tuple):
    """Hold the different parts of a minecraft command."""
    __slots__ = ()

    def __str__(self):
        return ' '.join(str(arg).replace('\n', ' ').strip() for arg in self)


class ExecutionContext(tuple):
    def get_prefix(self, ctx):
        if self is ctx[self.__class__]:
            return ()
        return self and ('execute', *sum(self, ()), 'run')


class CommandMixin(BasicCommandMixin):
    """Expose context-modifying methods that mirror minecraft commands."""

    def __init__(self, *args, ctx, execution_context=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

        if execution_context is None:
            execution_context = ExecutionContext()
        self.execution_context = execution_context

        self._stack = []

    def run(self, *args):
        self.ctx[FunctionBuilder].register_command(
            Command(self.execution_context.get_prefix(self.ctx) + args)
        )

    def execute(self, *clauses):
        return self.__class__(ctx=self.ctx, execution_context=ExecutionContext(clauses))

    @contextmanager
    def _using_execution_context(self):
        parent = self.ctx[FunctionBuilder]

        with FunctionBuilder(parent, next(parent.function_names), []).current() as builder:
            previous_context = self.ctx[ExecutionContext]
            self.ctx[ExecutionContext] = self.execution_context
            yield self
            self.ctx[ExecutionContext] = previous_context
            builder.build()

        self.run('function', builder.name)

    def __enter__(self):
        frame = self._using_execution_context()
        self._stack.append(frame)
        return frame.__enter__() # pylint: disable = no-member

    def __exit__(self, exc_type, exc_val, exc_tb):
        frame = self._stack.pop()
        return frame.__exit__(exc_type, exc_val, exc_tb)
