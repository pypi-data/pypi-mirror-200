from typing import Type
from sqlalchemy import create_engine
from os import environ
from .Helper import psql_insert_copy,timing

@timing
def load_cloud(df:Type) -> None:
    """
    Ira fazer o processo de carregamento para o RDS depois de processado.
    """
    
    engine = create_engine(f"postgresql://tracking:{environ['SQL_PASSWORD']}@prd-avi-chatbot-tracking-replica.cybqqoxm5ee1.us-east-1.rds.amazonaws.com/clean_data")

    df.to_sql('residential_tracking_treated',engine,if_exists = 'append',method = psql_insert_copy,index = False,chunksize = 10000)