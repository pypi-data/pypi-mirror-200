from typing import Callable, TYPE_CHECKING

import numpy as np

from .utilities import mask_infs
from .base import BaseQuery
if TYPE_CHECKING:
    pass

__all__ = ['sum', 'max', 'min', 'mean', 'std', 'count', 'any', 'all', 'exists', 'array']

python_any = any
python_all = all
python_max = max
python_min = min
python_sum = sum


def _template_aggregator(string_op, predicate, python_func: Callable, item: BaseQuery, wrt: BaseQuery = None,
                         remove_infs: bool = True, expected_dtype: str = None, returns_dtype:str = None,
                         op_name=None, distinct=False, nulls=False, args=None, kwargs=None):
    from ..data import Data
    from .objects import AttributeQuery
    if isinstance(wrt, Data):
        wrt = None
    elif isinstance(wrt, AttributeQuery):
        raise TypeError(f"Cannot aggregate {item} with respect to an attribute {wrt}. You can only aggregate with respect to an object.")
    if op_name is None:
        op_name = string_op
    try:
        return item._aggregate(wrt, string_op, op_name, predicate, expected_dtype, returns_dtype, remove_infs, distinct, nulls=nulls)
    except AttributeError:
        if distinct:
            item = set(item)
        return python_func(item, *args, **kwargs)


def sum(item, wrt=None, *args, **kwargs):
    return _template_aggregator('sum', False, python_sum, item, wrt, expected_dtype='number', args=args, kwargs=kwargs)


def max(item, wrt=None, *args, **kwargs):
    return _template_aggregator('max', False, python_max, item, wrt, expected_dtype='number', args=args, kwargs=kwargs)


def min(item, wrt=None, *args, **kwargs):
    return _template_aggregator('min', False, python_min, item, wrt, expected_dtype='number', args=args, kwargs=kwargs)


def count(item, wrt=None, *args, **kwargs):
    return _template_aggregator('count', False, len, item, wrt, returns_dtype='integer', args=args, kwargs=kwargs)


def exists(item, wrt=None, *args, **kwargs):
    return _template_aggregator('count', False, len, item, wrt, returns_dtype='number', args=args, kwargs=kwargs) > 0


def std(item, wrt=None, *args, **kwargs):
    return _template_aggregator('stDev', False, np.std, item, wrt, expected_dtype='number', args=args, kwargs=kwargs)


def mean(item, wrt=None, *args, **kwargs):
    return _template_aggregator('avg', False, np.mean, item, wrt, expected_dtype='number', op_name='mean',
                                args=args, kwargs=kwargs)

#predicates

def all(item, wrt=None, *args, **kwargs):
    return _template_aggregator('all', True, python_all, item, wrt, args=args, returns_dtype='boolean', expected_dtype='boolean', kwargs=kwargs)


def any(item, wrt=None, *args, **kwargs):
    return _template_aggregator('any', True, python_any, item, wrt, args=args, returns_dtype='boolean', expected_dtype='boolean', kwargs=kwargs)


def array(item, wrt=None, distinct=False, nulls=True, *args, **kwargs):
    return _template_aggregator('collect', False, list, item, wrt, distinct=distinct, nulls=nulls, args=args, kwargs=kwargs)