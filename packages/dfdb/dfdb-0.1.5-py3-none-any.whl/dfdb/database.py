import importlib
import contextlib
import warnings

import sqlalchemy as sa
import hyclib as lib

from . import config
from .dataframe import DataFrame

config = config['database']

__all__ = ['Database']

# @lib.clstools.init_repr
class Database:
    cfg = config['Database']
    def __init__(self, engine_kwargs=None, connect_kwargs=None):
        engine_kwargs = self.cfg['__init__']['engine_kwargs'] | ({} if engine_kwargs is None else engine_kwargs)
        connect_kwargs = self.cfg['__init__']['connect_kwargs'] | ({} if connect_kwargs is None else connect_kwargs)
        self.kwargs = {'engine_kwargs': engine_kwargs, 'connect_kwargs': connect_kwargs}
        connect_kwargs = {} if connect_kwargs is None else connect_kwargs
        self.engine = sa.create_engine(sa.URL.create(**engine_kwargs), connect_args=connect_kwargs)
        self._metadata = sa.MetaData()
        self.connection = None
        
        if self.engine.dialect.name == 'sqlite':
            with self.connect() as con:
                con.execute(sa.text('PRAGMA case_sensitive_like=ON'))
        else:
            warnings.warn("Case sensitive search currently not gauaranteed for dialects other than sqlite.")
        
    @property
    def metadata(self):
        with self.connect() as con:
            self._metadata.clear()
            self._metadata.reflect(con)  # update metadata
        return self._metadata
        
    @property
    def tables(self):
        return self.metadata.tables
        
    def __enter__(self):
        self.connection = self.engine.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
        
    @contextlib.contextmanager
    def connect(self):
        if self.connection is None:
            try:
                self.connection = self.engine.connect()
                yield self.connection
            finally:
                self.connection.commit()
                self.connection.close()
                self.connection = None
        else:
            try:
                yield self.connection
            finally:
                pass
        
    def __getitem__(self, key):
        table = self.tables[key]
        return DataFrame(self, sa.select(table))
    
    def __setitem__(self, key, value):
        with self.connect() as con:
            value.to_sql(key, con=con, if_exists='replace', index=False)
            
    def __delitem__(self, key):
        with self.connect() as con:
            self.tables[key].drop(con)
        
    def __repr__(self):
        kwargs = ", ".join(f'{k}={repr(v)}' for k, v in self.kwargs.items())
        return f'{type(self).__name__}({kwargs})'