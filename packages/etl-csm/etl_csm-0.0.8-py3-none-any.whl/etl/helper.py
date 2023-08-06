from typing import Type
from functools import wraps
from time import time
from logging import info

def timing(f):
    # Decorator simples para medir tempo de excecucao de funcao
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        info(f'Funcao {f.__name__} demoro {te-ts:2.4f} segundos')
        return result
    return wrap

def helper_columns(cursor:Type) -> Type:
    # Funcao simples para extracao de nomenclatura de colunas
    # Para formar dataframe
    cols = []
    for col in cursor.description:
        cols.append(col[0])
    return cols

