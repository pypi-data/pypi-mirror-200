import inspect
import string
from functools import wraps
from typing import Optional, Any

from .event import Event
from .format_dict import format_dict

__all__ = [
    'default',
    'named_default',
    'dynamic_default_args',
]

_empty = __import__('inspect')._empty


# noinspection PyPep8Naming
class default(Event):
    __slots__ = '_value'

    def __init__(self, value):
        super().__init__()
        self._value = value

    def __repr__(self):
        return repr(self._value)

    def __eq__(self, other):
        if isinstance(other, default):
            return self._value == other._value
        return self._value == other

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.emit(value)


class _NamedDefaultMeta(type):
    _instances = {}

    def _get_init_error_msg(cls, name, value, **kwargs):
        _init_error_msg = 'Define named default with one string and one value, ' \
                          'either by passing them as positional arguments ' \
                          '`{cls}([name], [value])`, as keywords ' \
                          '`{cls}(name=[name], value=[value])`, ' \
                          'or a single keyword argument `{cls}([name]=[value])`. ' \
                          '\nGot {cls}({args}).'
        _called_args = ''
        if name is not _empty:
            _called_args = f'name={name}'
            if value is not _empty:
                _called_args += ', '
        if value is not _empty:
            _called_args += f'value={value}'
        if len(_called_args) and len(kwargs):
            _called_args += ', '
        _called_args += ', '.join(f'{k}={v}' for k, v in kwargs.items())
        return _init_error_msg.format(cls=cls.__name__, args=_called_args)

    def __call__(cls, name=_empty, value=_empty, **kwargs):
        has_value = value is not _empty
        from_args = name is not _empty
        from_kwargs = len(kwargs) == 1
        if not from_args ^ from_kwargs:
            raise ValueError(cls._get_init_error_msg(name, value, **kwargs))
        if from_args:
            if not isinstance(name, str):
                raise ValueError(f'Name must be string. Got {type(name)}.')
            elif not has_value and name not in cls._instances:
                raise ValueError(f'{name} has not been registered.')
            value = value if has_value else None
        else:  # from_kwargs
            if has_value:
                raise ValueError(cls._get_init_error_msg(name, value, **kwargs))
            name, value = next(iter(kwargs.items()))
        if name not in cls._instances:
            cls._instances[name] = super(_NamedDefaultMeta, cls).__call__(name, value)
        return cls._instances[name]


# noinspection PyPep8Naming
class named_default(default, metaclass=_NamedDefaultMeta):
    """A named default object that holds a default value
    for arguments, which can be dynamically changed later.

    The constructor accepts passing two positional arguments name
    and value. If value is not provided and the name hasn't been
    registered, an Exception will be raised.

    >>> x = named_default('x', 0.5)

    Or more expressively:

    >>> x = named_default(name='x', value=0.5)

    Ortherwise, use a single keyword argument. The keyword will
    be used as name.

    >>> x = named_default(x=1)

    For modifying the default values everywhere, call this function
    with only the name of defined variable. Any value provided will
    have no effect.

    >>> named_default('x').value = 2.0
    """

    __slots__ = 'name'

    def __init__(self,
                 name: Optional[str] = None,
                 value: Optional[Any] = None,
                 **kwargs):
        super().__init__(value)
        self.name = name


def dynamic_default_args(format_doc=True, force_wrap=False):
    """
    A decorator for substituting function with dynamic default
    arguments with minimal overhead.

    It can also will modify the function's docstring with
    format keys automatically when any of the default args changes.

    >>> @dynamic_default_args(format_doc=True)
    >>> def foo(x=named_default(x=5))
    >>>     \"\"\"An exmaple function with docstring.
    >>>
    >>>     Args:
    >>>         x: Argument dynamically defaults to {x}.
    >>>     \"\"\"
    >>>     ...

    When the default value is changed later, both the default and
    the function's docstring will be updated accordingly.

    >>> named_default('x').value = 10
    >>> foo()
    10
    >>> help(foo)

    Args:
        format_doc: Automatically format the docstring of the
         decorated function or not. Defaults to ``True``.
        force_wrap: Wrap the decorated function even if there
         is no dynamic default argument or not.
         Defaults to ``False``.
    """

    def decorator(func):
        params = inspect.signature(func).parameters
        n_params = len(params)

        names = list(params.keys())
        default_vals = [v.default for v in params.values()]
        kinds = [v.kind for v in params.values()]
        default_mask = [True if v.default is not _empty else False
                        for v in params.values()]
        dynamic_default_mask = [True if isinstance(v.default, default) else False
                                for v in params.values()]
        del params

        has_dynamic_defaults = any(dynamic_default_mask)
        if force_wrap or has_dynamic_defaults:
            func_alias = 'func'
            wrapper_alias = 'wrapper'
            default_alias = default.__name__
            while func_alias in names:
                func_alias = '_' + func_alias
            while wrapper_alias in names:
                wrapper_alias = '_' + wrapper_alias
            while default_alias in names:
                default_alias = '_' + default_alias
            context = {
                default_alias: default,
                func_alias: func
            }

            expr = f'def {wrapper_alias}('
            for i, (name, kind, default_val) in enumerate(zip(names, kinds, default_vals)):
                if default_mask[i]:
                    context[f'{name}_'] = default_val
                expr += '{}{}'.format('*' if kind == 2 else '**' if kind == 4 else '', name)
                if default_val is not _empty:
                    expr += f'={name}_'
                if i < n_params - 1:
                    expr += ', '
            expr += f'): return {func_alias}('
            for i, (name, kind) in enumerate(zip(names, kinds)):
                if kind == 2:
                    expr += '*'
                elif kind == 4:
                    expr += '**'
                expr += name
                if kind == 3:
                    expr += f'={name}'
                if dynamic_default_mask[i]:
                    expr += f'._value if isinstance({name}, {default_alias}) else {name}'
                if i < n_params - 1:
                    expr += ', '
            expr += ')'
            exec_locals = {}
            exec(compile(expr, f'<{func.__name__}_wrapper>', 'exec'), context, exec_locals)
            wrapper = wraps(func)(exec_locals[wrapper_alias])
        else:  # no wrapping
            wrapper = func

        if format_doc and wrapper.__doc__ is not None:
            format_keys = set(_[1] for _ in string.Formatter().parse(wrapper.__doc__)
                              if _[1] is not None)
            format_keys = format_keys.intersection(names)
            if len(format_keys):
                # format docstring
                wrapper.__default_doc__ = wrapper.__doc__
                format_keys_ids = [i for i in range(n_params)
                                   if names[i] in format_keys and default_mask[i]]

                def update_docstring(*args, **kwargs):
                    wrapper.__doc__ = wrapper.__default_doc__.format_map(format_dict({
                        names[i]: default_vals[i]._value if dynamic_default_mask[i]
                        else default_vals[i] for i in format_keys_ids}))

                update_docstring()
                # automatic update later
                for i in format_keys_ids:
                    if dynamic_default_mask[i]:
                        default_vals[i].connect(update_docstring)

        return wrapper

    return decorator
