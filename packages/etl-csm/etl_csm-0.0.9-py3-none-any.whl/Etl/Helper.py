from typing import Type
from functools import wraps
from time import time
from logging import info
from io import StringIO
from csv import writer

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

def psql_insert_copy(table, conn, keys, data_iter):
    """
    Executa sql query unico para por dados de maneira eficiente em postgresql

    Parametros
    ----------
    table : pandas.io.sql.SQLTable - Tabela
    conn : sqlalchemy.engine.Engine ou sqlalchemy.engine.Connection
    keys : lista de strings com nomes das colunas, nao precisa passar
    data_iter : Iterador que vai fazer o trampo todo
    """
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer_obj = writer(s_buf)
        writer_obj.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join(['"{}"'.format(k) for k in keys])
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name
        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)
