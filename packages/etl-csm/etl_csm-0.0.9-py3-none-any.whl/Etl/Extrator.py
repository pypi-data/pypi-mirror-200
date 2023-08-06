import psycopg2
import pandas as pd
from os import environ
from sys import exit
from typing import Type
from .Helper import timing,helper_columns

class Connection:
    """
    Cria objeto de conexão e o atributo cursor a ser utilizado na funcao form_df_tracking, 
    ele também sera essencial para fazer a parte de carregamento dos dados de volta para o rds
    """
    @timing
    def __init__(self):
        try:
            engine = psycopg2.connect(
                database = 'postgres',
                user = 'tracking',
                password = environ['SQL_PASSWORD'],
                host = 'prd-avi-chatbot-tracking-replica.cybqqoxm5ee1.us-east-1.rds.amazonaws.com',
                port = '5432',
            )

        except (Exception,psycopg2.Error) as error:
            print(f'''
                Erro ao tentar fazer conexão com o dataframe!
                Verifique se você está conectado a VPN fortclient
                {error}
                ''',)
            exit(1)
        self.cursor = engine.cursor()
        
    @timing
    def form_df_tracking(self,query:str) -> type(pd.DataFrame):
        """
        Extrai os dados do RDS, e transforma em pandas object
        1- Extrai os dados do RDS,
        2- Roda o query (a ser definido)
        3- Pegas as colunas da tabela tracking
        4- Joga para um pandas object
        """
        self.cursor.execute(query)
        # Executando query, para obtencao de dados
        data = self.cursor.fetchall()
        cols = helper_columns(cursor = self.cursor)
        df = pd.DataFrame(data = data, columns = cols)
        if df.empty:
            raise Exception('O seu dataframe está vazio! Algo está de errado com o seu query')
        return df
    
@timing
def form_df_extras(df:Type):
    """  
    Explode os extras globais dentro coluna,
    global_extras_raw
    """
    new_df = pd.DataFrame(list(df['global_extras_raw']))
    if new_df.empty:
        raise Exception('O seu dataframe de extras está vazio! Verifique o seu query')
    return new_df



