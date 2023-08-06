from logging import basicConfig,INFO
from typing import Type
from pandas import concat
from .Helper import timing
from .Extrator import Connection,form_df_extras
from .Treatment_tracking import ensure_dtypes,dtype_tracking,remove_test,steps,errors,flag_duplicated_tracks
from .Treatment_extras import patternizing_columns,ensure_nan_extras,dtype_extras
from .Treatment_extras import fill_na_extras,patternizing_origins,form_extras_plan
from .Loader import load_cloud

class Runner:
    """
    Classe de execucao geral, faz tudo o puxada de dados o tratamento deles e carrega eles
    forma de evitar arquivos salvos em memoria local.
    """
    def __init__(self,query:str) -> Type:
        """
        Executor dessa funcao
        query = string sql de extracao do RDS
        """
        self.query = query
        basicConfig(filename='etl.log',filemode='a',level=INFO, format='%(levelname)s: %(message)s',)
        # Configurando logs

    def etl_df(self):
        """
        Funcao que roda ETL do dataframe tracking,
        nao arquiva em memoria o dataframe extras_df
        """
        #1
        connection = Connection()
        #2
        df = connection.form_df_tracking(self.query)
        #3
        df = ensure_dtypes(df)
        #4
        # df = remove_test(df)
        #  Não se pode remover testes no ambiente de teste porque senao você remove todo mundo
        #5
        flag_duplicated_tracks(df)
        #6
        df = dtype_tracking(df)
        #7
        df['steps'] = steps(df['category'])
        #8
        df['errors'] = errors(df['category'])
        return df
        # Sim esses objetos sao acessiveis se voce quiser

    def etl_extras_df(self,df:Type) -> Type:
        """
        Funcao que roda ETL do dataframe extras
        """
        #1
        extras_df = form_df_extras(df)
        #2
        extras_df = patternizing_columns(extras_df)
        #3
        extras_df = ensure_nan_extras(extras_df)
        #4
        extras_df = fill_na_extras(extras_df)
        #5
        extras_df = dtype_extras(extras_df)
        #6
        extras_df = patternizing_origins(extras_df)
        #7
        extras_df = form_extras_plan(extras_df)
        return extras_df
    
    def run(self) -> None:
        """
        Funcao que roda tudo
        """
        df = self.etl_df()
        extras_df = self.etl_extras_df(df)
        df = concat([df,extras_df],axis = 1)

        load_cloud(df)
