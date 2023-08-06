from collections import OrderedDict, Counter, defaultdict
from pathlib import Path
from typing import List, Union, Tuple

import numpy as np
import py2neo
from astropy.io import fits, registry
from astropy.table import Table as AstropyTable, Row as AstropyRow, MaskedColumn as AstropyMaskedColumn
from py2neo.cypher import Cursor


def ragged_array(data):
    """
    Given an object array of different length lists/arrays (indexed on the first axis) return a ragged array
    where unaligned elements are filled with NaN.
    e.g.:
    >>> ragged_array([[1, 2, 3], [4, 5, 6, 7]])
    np.mask.array([[1, 2, 3, --], [4, 5, 6, 7]], mask=[[False, False, False, True], [False, False, False, False]])
    """
    darrays = [np.ma.asarray(d) for d in data]
    dtypes = {d.dtype for d in darrays if not np.all(d.mask)}
    if not dtypes:
        dtype = np.float_
    else:
        dtype = np.stack([np.array([], dtype=d) for d in dtypes]).dtype
    shapes = [d.shape for d in darrays]
    if len(set(shapes)) == 1:
        return data
    maxshape = np.max(shapes, axis=0)
    array = np.ma.empty((len(data), *maxshape), dtype=dtype)
    array.mask = True
    slcs = [tuple(slice(0, s) for s in shape_tuple) for shape_tuple in shapes]
    for i, (slc, d) in enumerate(zip(slcs, data)):
        array.__setitem__((i, *slc), d)
    return array


def ragged_column(data, name):
    return MaskedColumn(ragged_array(data), name=name)


class ColnameParser:
    def __init__(self, parent, partial_colname: str):
        self.parent = parent
        self.partial_colname = partial_colname

    def __getattr__(self, colname):
        return self.parent.__getattr__(self.partial_colname + '.' + colname)


class DotHandlerMixin:
    def __getattr__(self, attr):
        if attr in self.colnames:
            return self[attr]
        if any(colname.startswith(attr) for colname in self.colnames if '.' in colname):
            return ColnameParser(self, attr)
        return super(DotHandlerMixin, self).__getattribute__(attr)


class Row(DotHandlerMixin, AstropyRow):
    pass


class MaskedColumn(AstropyMaskedColumn):
    def apply(self, func, *args, **kwargs) -> 'MaskedColumn':
        """
        Apply a function to each row in the column. Returns nd array if possible otherwise an unstructured array.
        :param func: Callable to apply to each row. Takes an array/scalar depending on the type of the column.
        """
        return ragged_column([func(d, *args, **kwargs) for d in self.data], self.name)

    def masked(self, mask, inplace=False):
        if inplace:
            c = self
        else:
            c = self.copy()
        c.mask |= mask
        return c

    def filtered(self, filt, inplace=False):
        if inplace:
            c = self
        else:
            c = self.copy()
        c.mask |= ~filt
        return c


class Table(DotHandlerMixin, AstropyTable):  # allow using `.` to access columns
    Row = Row
    Column = MaskedColumn

    def apply(self, func, *args, **kwargs) -> 'MaskedColumn':
        """
        Apply a function to each row in the column. Returns nd array if possible otherwise an unstructured array.
        :param func: Callable to apply to each row. Takes an array/scalar depending on the type of the column.
        """
        return ragged_column([func(row, *args, **kwargs) for row in self], func.__name__)

class ArrayHolder:
    def __init__(self, array):
        self.array = array


def vstack_rows(rows: List[Tuple[List, List[bool], List[str]]], *args, **kwargs) -> Table:
    # for each column, remove null rows, make table, put nulls back in
    columns, names = zip(*rows)
    names = names[0]
    columns = list(zip(*columns))
    duplicate_names = [n for n, i in Counter(names).items() if i > 1]
    counter = defaultdict(int)
    _names = []
    for n in names:
        if n in duplicate_names:
            _names.append(f"{n}{counter[n]}")
            counter[n] += 1
        else:
            _names.append(n)
    return Table([ragged_column(c, f"{n}{counter.get(n, '')}") for c, n in zip(columns, _names)])

def int_or_slice(x: Union[int, float, slice, None]) -> Union[int, slice]:
    if isinstance(x, (int, float)):
        return int(x)
    elif isinstance(x, slice):
        return x
    else:
        return slice(None, None)

class FileHandler:
    def __init__(self, rootdir: Union[Path, str], max_concurrency: int = 1000):
        self.rootdir = Path(rootdir)
        self.max_concurrency = max_concurrency
        self.files = OrderedDict()

    def read(self, filename: Union[Path, str], ext: Union[float, int, str] = None, index: Union[float, int, slice] = None,
             key: Union[str, int, float, slice] = None, header_only=False):
        f = self.open_file(filename)
        if ext is None:
            ext = 0
        ext = ext if isinstance(ext, str) else int(ext)
        hdu = f[ext]
        index = int_or_slice(index)
        key = key if isinstance(key, str) else int_or_slice(key)
        if header_only:
            if key is not None:
                return hdu.header[key]
            return hdu.header
        return hdu.data[index][key]


    def open_file(self, filename: Union[Path, str]):
        filename = self.rootdir / Path(filename)
        if filename in self.files:
            return self.files[filename]
        else:
            if len(self.files) >= self.max_concurrency:
                self.close_file(next(iter(self.files)))
            self.files[filename] = fits.open(str(filename), memmap=True)
            return self.files[filename]

    def close_file(self, filename: Path):
        if filename in self.files:
            del self.files[filename]

    def close_all(self):
        for filename in list(self.files):
            self.close_file(filename)

    def __del__(self):
        self.close_all()


def recursive_replace_None(l: List) -> List:
    if not isinstance(l, list):
        return np.ma.masked if l is None else l
    for i, item in enumerate(l):
        l[i] = recursive_replace_None(item)
    return l


class RowParser(FileHandler):
    def parse_product_row(self, row: py2neo.cypher.Record, names: List[Union[str, None]], is_products: List[bool],
                          as_row: bool):
        """
        Take a pandas dataframe and replace the structure of ['fname', 'extn', 'index', 'key', 'header_only']
        with the actual data
        """
        columns = []
        colnames = []
        for value, cypher_name, name, is_product in zip(row.values(), row.keys(), names, is_products):
            if is_product:
                if value is not None:
                    if isinstance(value[0], list):  # i.e. its a list of product addresses that have been collected
                        value = [self.read(*v) for v in value]
                    else:
                        value = self.read(*value)
            value = recursive_replace_None(value)
            name = cypher_name if name is None or name == 'None' else name
            mask = value is None or np.size(value) == 0
            try:
                mask = mask | ~np.isfinite(value)
            except TypeError:
                pass
            value = np.ma.where(~mask, np.ma.asarray(value), np.ma.masked)
            columns.append(value)
            colnames.append(name)
        if as_row:
            columns = [MaskedColumn([value]) for value in columns]
            return Table(columns, names=colnames)[0]
        return columns, colnames

    def iterate_cursor(self, cursor: Cursor, names: List[Union[str, None]], is_products: List[bool], as_row: bool):
        for row in cursor:
            yield self.parse_product_row(row, names, is_products, as_row)

    def parse_to_table(self, cursor: Cursor, names: List[str], is_products: List[bool]):
        rows = list(self.iterate_cursor(cursor, names, is_products, False))
        if not rows:
            return Table([MaskedColumn([], name=name) for name in names])
        return vstack_rows(rows)


def apply(obj, func, *args, **kwargs):
    """Applies the function to a table or column"""
    return getattr(obj, 'apply')(func, *args, **kwargs)

def filtered(column, filt):
    """Filters a masked column based on a boolean array where False means masked"""
    return column.filtered(filt)

def masked(column, mask):
    """Masks a masked column based on a boolean array where True means masked"""
    return column.masked(mask)


def identifier(origin, filepath, fileobj, *args, **kwargs):
    return registry._identifiers[('fits', AstropyTable)](origin, filepath, fileobj, *args, **kwargs)


def reader(input, hdu=None, astropy_native=False, memmap=False, character_as_bytes=True):
    original = registry.get_reader('fits', AstropyTable)
    table = original(input, hdu=hdu, astropy_native=astropy_native, memmap=memmap, character_as_bytes=character_as_bytes)
    for colname, fill_value, nan_mask in zip(table.meta['_masked_columns'], table.meta['_fill_values'], table.meta['_nan_masked']):
        if nan_mask:
            fill_value = np.nan
            mask = np.isnan(table[colname])
        else:
            mask = table[colname] == fill_value
        table[colname] = MaskedColumn(table[colname], fill_value=fill_value, mask=mask)
    return table

def writer(input, output, overwrite=False):
    original = registry.get_writer('fits', AstropyTable)
    input.meta['_masked_columns'] = []
    input.meta['_fill_values'] = []
    input.meta['_nan_masked'] = []
    for colname in input.colnames:
        if isinstance(input[colname], MaskedColumn):
            input.meta['_masked_columns'].append(colname)
            try:
                if np.isnan(input[colname].fill_value):
                    input.meta['_nan_masked'].append(True)
                    input.meta['_fill_values'].append(0.)
                    continue
            except TypeError:
                pass
            input.meta['_fill_values'].append(input[colname].fill_value)
            input.meta['_nan_masked'].append(False)
    return original(input, output, overwrite)

#
# registry.register_identifier('fits', Table, identifier, force=True)
# registry.register_reader('fits', Table, reader, force=True)
# registry.register_writer('fits', Table, writer, force=True)