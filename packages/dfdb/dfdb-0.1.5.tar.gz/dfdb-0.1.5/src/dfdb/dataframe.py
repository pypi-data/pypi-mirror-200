import collections
import itertools
import functools
import sys

import pandas as pd
import numpy as np
import sqlalchemy as sa

from . import (
    abc,
    parsing,
)

class DataFrame(abc.SQL):
    def __init__(self, db, sql):
        super().__init__(db, sql)
        self._table = self.sql.subquery()
    
    def fetch(self):
        with self.db.connect() as con:
            cur = con.execute(self.sql)
            rows = cur.fetchall()
        return pd.DataFrame(rows, columns=cur.keys())
    
    @property
    def table(self):
        return self._table
    
    @property
    def columns(self):
        return tuple(c.name for c in self.table.c)
    
    def items(self):
        for k in self.columns:
            yield k, self[k]
    
    def info(self):
        info = pd.DataFrame([{
            'column': c.name,
            'type': c.type,
            'default': c.default,
            'nullable': c.nullable,
            'unique': c.unique,
            'primary_key': c.primary_key,
            'foreign_keys': c.foreign_keys,
            'constraints': c.constraints,
            'autoincrement': c.autoincrement,
            'computed': c.computed,
        } for c in self.table.c])
        return info
        
    def __getitem__(self, key):
        if key is Ellipsis:
            col_key, row_key = slice(None), slice(None)
        elif isinstance(key, tuple):
            col_key, row_key = key
        else:
            col_key, row_key = key, slice(None)
            
        if col_key is Ellipsis:
            col_key = slice(None)
            
        if row_key is Ellipsis:
            row_key = slice(None)
            
        if isinstance(col_key, str) and isinstance(row_key, int):
            result_class = Item
        elif isinstance(col_key, str):
            result_class = Column
        elif isinstance(row_key, int):
            result_class = Row
        else:
            result_class = DataFrame
            
        if isinstance(col_key, slice):
            if not (col_key.start is None and col_key.stop is None and col_key.step is None):
                raise ValueError(f"col_key can only be a slice if start, stop, and step are all None, but {col_key=}.")
            sql = sa.select(self.table)
        elif isinstance(col_key, str):
            sql = sa.select(self.table.c[col_key])
        elif isinstance(col_key, collections.abc.Iterable):
            sql = sa.select(*self.table.c[tuple(col_key)])
        else:
            raise TypeError(f"col_key must be a str, slice, Ellipsis, or Iterable, but {type(col_key)=}.")

        if isinstance(row_key, IndexableColumn):
            sql = sql.where(row_key.column)
        elif isinstance(row_key, int):
            start, stop = row_key, row_key + 1
            sql = sql.slice(start, stop)
        elif isinstance(row_key, slice):
            if row_key.step is not None:
                raise ValueError(f"row_key can only be a slice if step is None, but {row_key=}.")
            start = 0 if row_key.start is None else row_key.start
            stop = -1 if row_key.stop is None else row_key.stop
            sql = sql.slice(start, stop)
        else:
            raise TypeError(f"row_key must be an IndexableColumn, int, slice, or Ellipsis, but {type(row_key)=}.")
            
        if result_class is Column:
            if isinstance(row_key, slice) and row_key.start is None and row_key.stop is None:
                return IndexableColumn(self.db, self.table.c[col_key])
            return Column(self.db, sql)
            
        return result_class(self.db, sql)
    
    def merge(self, df, how='inner', sort=False, on=None, left_on=None, right_on=None, suffixes=('_x', '_y')):
        if how == 'cross':
            if not on is None and left_on is None and right_on is None:
                raise ValueError(f"on, left_on, and right_on must all be None when how == 'cross', but {on=}, {left_on=}, {right_on=}.")
                
            overlap = [col for col in self.columns if col in df.columns]
            left_cols = [self.table.c[col].label(f'{col}{suffixes[0]}') if col in overlap else self.table.c[col] for col in self.columns]
            right_cols = [df.table.c[col].label(f'{col}{suffixes[1]}') if col in overlap else df.table.c[col] for col in df.columns]
            sql = sa.select(*left_cols, *right_cols)
            
            return DataFrame(self.db, sql)
        
        if on is not None:
            if not (left_on is None and right_on is None):
                raise ValueError(f"left_on and right_on must be None when on is not None, but {left_on=}, {right_on=}.")
            left_on, right_on = on, on
            
        if (left_on is None and right_on is not None) or (left_on is not None and right_on is None):
            raise ValueError(f"left_on and right_on must either be both None or not None, but {left_on=}, {right_on=}.")
        
        if left_on is None: # right_on must also be None
            on = [column for column in self.columns if column in df.columns] # same order as left df
            left_on, right_on = on, on
        else:
            left_on, right_on = np.atleast_1d(left_on), np.atleast_1d(right_on)
            if len(left_on) != len(right_on):
                raise ValueError(f"Length of left_on must be same as length of right_on, but {len(left_on)=}, {len(right_on)=}.")
                
        left, right = self.table, df.table
        if sort:
            left = sa.select(left, sa.func.row_number().over().label('row_number')).subquery()
            right = sa.select(right, sa.func.row_number().over().label('row_number')).subquery()
        
        cond = functools.reduce(lambda x, y: x & y, [left.c[lcol] == right.c[rcol] for lcol, rcol in zip(left_on, right_on)])
        
        if how == 'inner':
            table = left.join(right, cond)
        elif how == 'left':
            table = left.join(right, cond, isouter=True)
        elif how == 'right': 
            table = right.join(left, cond, isouter=True)
        elif how == 'outer':
            table = left.join(right, cond, full=True)
        else:
            raise ValueError(f"how must be either 'inner', 'left', 'right', 'outer', or 'cross', but {how=}.")
            
        on = [lcol for lcol, rcol in zip(left_on, right_on) if lcol == rcol]
        left_cols = [left.c[col].label(f'{col}{suffixes[0]}') if (col in df.columns and col not in on) else left.c[col] for col in self.columns]
        right_cols = [right.c[col].label(f'{col}{suffixes[1]}') if col in self.columns else right.c[col] for col in df.columns if col not in on]
        sql = sa.select(*left_cols, *right_cols).select_from(table)
        
        if sort:
            if how == 'right':
                sql = sql.order_by(*[right.c[col] for col in right_on if col not in on], *[left.c[col] for col in left_on], right.c.row_number, left.c.row_number)
            else:
                sql = sql.order_by(*[left.c[col] for col in left_on], *[right.c[col] for col in right_on if col not in on], left.c.row_number, right.c.row_number)
            
        return DataFrame(self.db, sql)
    
    def sort_values(self, by):
        return DataFrame(self.db, self.sql.order_by(by))
    
    def groupby(self, columns):
        return DataFrameGroupBy(self, columns)
    
    def eval(self, condition, level=0):
        condition = parsing.preparse(condition)
        var_names = parsing.parse_var_names(condition)
        frame = sys._getframe(level+1) # see https://github.com/pandas-dev/pandas/blob/main/pandas/core/computation/scope.py
        env = frame.f_globals | frame.f_locals
        
        # add @ variables
        var_dict = {f'{parsing.LOCAL_TAG}{k}': env[k] for k in var_names}
        
        # add dataframe columns
        var_dict = var_dict | {parsing.clean_column_name(k): v for k, v in self.items() if not isinstance(k, int)}
        
        return eval(condition, var_dict)
    
    def query(self, condition, level=0):
        return self[:,self.eval(condition, level=level+1)]
    
    
class DataFrameGroupBy:
    def __init__(self, df, columns):
        self.df = df
        self.columns = tuple(columns)
        self.ungrouped_columns = tuple(col for col in self.df.columns if col not in self.columns)
    
    def __getitem__(self, key):
        if not isinstance(key, str):
            raise NotImplementedError(f"Currently only supports string key, but {key=}.")
        return ColumnGroupBy(self, key)
    
    @property
    def nth(self):
        return GroupByNthSelector(self)
    
    def agg(self, *args, **kwargs):
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                new_args += [(col, arg) for col in self.ungrouped_columns]
            elif isinstance(arg, tuple):
                new_args.append(arg)
            else:
                raise TypeError(f"arg must be a string or a 2-tuple, but {arg=}.")
        args = new_args
        
        columns = []
        for k, v in itertools.chain(zip(args, args), kwargs.items()):
            k = f'{k[0]}_{k[1]}' if isinstance(k, tuple) else k
            column, func = v
                
            if func == 'mean':
                func = 'avg'
            func = getattr(sa.func, func)
            
            column = func(self.df.table.c[column]).label(k)
            columns.append(column)
        
        return DataFrame(self.df.db, sa.select(*self.df.table.c[self.columns], *columns).group_by(*self.columns))
        
    def transform(self, *args, **kwargs):
        raise NotImplementedError()
        
    def nunique(self):
        return DataFrame(self.df.db, sa.select(*self.df.table.c[self.columns], *[sa.func.count(self.df.table.c[col].distinct()).label(col) for col in self.ungrouped_columns]).group_by(*self.columns))
    
    def count(self):
        return self.agg('count')
    
    def sum(self):
        return self.agg('sum')
    
    def mean(self):
        return self.agg('mean')
    
class GroupByNthSelector:
    def __init__(self, gb):
        self.gb = gb
        
    def __getitem__(self, key):
        if isinstance(key, int):
            start, stop = key, key + 1
        elif isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = -1 if key.stop is None else key.stop
        else:
            raise KeyError(f"key must be an int or a slice, but {type(key)=}.")
            
        df = sa.select(self.gb.df.table, sa.func.row_number().over(partition_by=self.gb.columns).label('row_number'), sa.func.row_number().over().label('order')).subquery()
        return DataFrame(self.gb.df.db, sa.select(*df.c[self.gb.df.columns]).where(df.c.row_number.between(start, stop)).order_by(df.c.order))
    
    
class ColumnGroupBy:
    def __init__(self, gb, column):
        self.gb = gb
        self.column = column
        
    def nunique(self):
        return Column(self.gb.df.db, sa.select(sa.func.count(self.gb.df.table.c[self.column].distinct())).group_by(*self.gb.columns))
    
    def count(self):
        return self.agg('count')
    
    def sum(self):
        return self.agg('sum')
    
    def mean(self):
        return self.agg('mean')
 
    def agg(self, *args, **kwargs):
        columns = []
        for v in itertools.chain(args, kwargs.items()):
            k, v = v if isinstance(v, tuple) else (v, v)
                
            if v == 'mean':
                v = 'avg'
            func = getattr(sa.func, v)
            
            column = func(self.gb.df.table.c[self.column]).label(k)
            columns.append(column)

        if len(columns) == 1:
            return Column(self.gb.df.db, sa.select(*columns).group_by(*self.gb.columns))
        
        return DataFrame(self.gb.df.db, sa.select(*self.gb.df.table.c[self.gb.columns], *columns).group_by(*self.gb.columns))
    
    def transform(self, *args, **kwargs):
        columns = []
        for v in itertools.chain(args, kwargs.items()):
            k, v = v if isinstance(v, tuple) else (v, v)
                
            if v == 'mean':
                v = 'avg'
            func = getattr(sa.func, v)
            
            column = func(self.gb.df.table.c[self.column]).over(partition_by=self.gb.columns).label(k)
            columns.append(column)
            
        result_class = Column if len(columns) == 1 else DataFrame
        
        return result_class(self.gb.df.db, sa.select(*columns).order_by(sa.func.row_number().over()))
    

class Column(abc.SQL):
    def fetch(self):
        with self.db.connect() as con:
            rows = con.execute(self.sql).fetchall()
        return np.array(rows).squeeze()
    
    
def decorator(func):
    @functools.wraps(func)
    def wrapped(self, *args):
        args = [arg.column if isinstance(arg, IndexableColumn) else arg for arg in args]
        expr = func(self.column, *args)
        return IndexableColumn(self.db, expr)
    return wrapped
    

class IndexableColumn(Column):
    def __init__(self, db, column):
        self.db = db
        self.column = column
    
    @property
    def str(self):
        return StringMethods(self.db, self.column)
    
    @property
    def sql(self):
        return sa.select(self.column)
    
    def unique(self):
        return Column(self.db, sa.select(self.column.distinct()))
    
    @decorator
    def __add__(self, x):
        return self + x
    
    @decorator
    def __sub__(self, x):
        return self - x
    
    @decorator
    def __mul__(self, x):
        return self * x
    
    @decorator
    def __truediv__(self, x):
        return self / x
    
    @decorator
    def __and__(self, x):
        return self & x
    
    @decorator
    def __or__(self, x):
        return self | x
    
    @decorator
    def __xor__(self, x):
        return self ^ x
    
    @decorator
    def __radd__(self, x):
        return x + self
    
    @decorator
    def __rsub__(self, x):
        return x - self
    
    @decorator
    def __rmul__(self, x):
        return x * self
    
    @decorator
    def __rtruediv__(self, x):
        return x / self
    
    @decorator
    def __rand__(self, x):
        return x & self
    
    @decorator
    def __ror__(self, x):
        return x | self
    
    @decorator
    def __rxor__(self, x):
        return x ^ self
    
    @decorator
    def __eq__(self, x):
        return self == x
    
    @decorator
    def __ne__(self, x):
        return self != x
    
    @decorator
    def __lt__(self, x):
        return self < x
    
    @decorator
    def __le__(self, x):
        return self <= x
    
    @decorator
    def __gt__(self, x):
        return self > x
    
    @decorator
    def __ge__(self, x):
        return self >= x
    
    @decorator
    def __neg__(self):
        return -self
    
    @decorator
    def __pos__(self):
        return +self
    
    @decorator
    def __invert__(self):
        return ~self
    

class StringMethods(IndexableColumn):
    @decorator
    def contains(self, pat):
        return self.like(f'%{pat}%')
    
    @decorator
    def startswith(self, pat):
        return self.like(f'{pat}%')
    
    @decorator
    def endswith(self, pat):
        return self.like(f'%{pat}')
    
      
class Row(abc.SQL):
    def fetch(self):
        with self.db.connect() as con:
            row = con.execute(self.sql).fetchone()
        return row
    

class Item(abc.SQL):
    def fetch(self):
        with self.db.connect() as con:
            row = con.execute(self.sql).fetchone()
        return row[0]