import abc

import hyclib as lib

@lib.clstools.attr_repr
class SQL(abc.ABC):
    def __init__(self, db, sql):
        self.db = db
        self.sql = sql

    def __str__(self):
        newline = '\n    '
        aligned = {k: str(v).replace('\n', newline + ' '*(len(k) + 1)) for k, v in self.__dict__.items()}
        attrs = f",{newline}".join(f"{k}={v}" for k, v in aligned.items())
        return f'{type(self).__name__}({newline}{attrs}\n)'
    
    @abc.abstractmethod
    def fetch(self):
        pass
    