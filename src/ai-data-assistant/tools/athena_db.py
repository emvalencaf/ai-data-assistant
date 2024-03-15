import os

from dotenv import load_dotenv

from typing import List
from langchain.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine, inspect


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")

class AthenaDB:
    def __init__(self):
        port = int(os.getenv("ATHENA_PORT"))
        schema = os.getenv("ATHENA_SCHEMA")
        S3_staging = os.getenv("ATHENA_STAGING")
        wkgroup = os.getenv("ATHENA_WORK_GROUP")
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID") # When import that code to a lambda function comment on that line
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY") # When import that code to a lambda function comment on that line

        conn_credentials = f"awsathena+rest://{aws_access_key_id}:{aws_secret_access_key}" # When import that code to a lambda function change to "awsathena+rest://"

        conn = f'athena.{AWS_REGION}.amazonaws.com:{port}'

        conn_str = f'{conn_credentials}@{conn}/{schema}?s3_staging_dir={S3_staging}&work_group={wkgroup}'

        self._engine = create_engine(conn_str, echo=False)
        self._db = SQLDatabase(engine=self._engine)

        self._tables = []  # Inicializar _tables como uma lista vazia

        self._set_table_schemas()
        
    @property
    def db(self):
        return self._db
    
    @property
    def tables(self) -> List:
        return self._tables
    
    def _set_table_schemas(self):
    
        # it will query to the Athena table info so the bot can correctly query to
        inspector = inspect(self._engine)
        
        tables = os.getenv("ATHENA_TABLE_NAME").split(",")
        
        for table_name in tables:
            cols = [(col['name'], col['type']) for col in inspector.get_columns(table_name=table_name) if col['name'].find("partition")]
        
            table_schema = f"CREATE TABLE {table_name} (\n"
            
            for i, (col_name, col_type) in enumerate(cols):
                table_schema += f'{col_name} {col_type}{", " if i != len(cols) - 1 else ""}\n'
            
            table_schema += ')'
            
            self._tables.append(table_schema)  # Adicionar esquema da tabela à lista _tables
