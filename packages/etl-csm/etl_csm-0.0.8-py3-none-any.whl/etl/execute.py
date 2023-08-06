from logging import basicConfig,INFO
from typing import Type
from .helper import timing
from .extrator import Connection,form_df_extras
from .treatment_tracking import ensure_dtypes,dtype_tracking,remove_test,steps,errors,flag_duplicated_tracks
from .treatment_extras import patternizing_columns,ensure_nan_extras,dtype_extras
from .treatment_extras import fill_na_extras,patternizing_origins,form_extras_plan

class Execute:
    """
    Classe de execucao para jupyter notebooks
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
        # Sim esses objetos so sao acessiveis se voce processar

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
    
if __name__ == '__main__':
    query = """ 
        SELECT *
        FROM tracking
        WHERE queued_date_service >= (timezone('ADT',NOW()) - INTERVAL '15 minutes')
    """
    obj = Execute(query=query)
    df = obj.etl_df()
    extras_df = obj.etl_extras_df(df)

    # print(df.head())
    # print(df.columns)
    # print(df.dtypes)
    # print(extras_df.head())
    # print(extras_df.columns)
    # print(extras_df.dtypes)