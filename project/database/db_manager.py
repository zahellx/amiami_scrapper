from .models.figure import Figure
from sqlalchemy import create_engine
import pandas as pd
from . import db
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

class DatabaseManager():
    # Para evitar jaleos, el tema es que se le pasara por aqui un nombre y con un Factory devolvieramos el modelo necesario
    def __init__(self, model):
        db = 'db'
        self.model = model
        self.table_name = model.__tablename__
        self.db_connection_str = f'mysql+pymysql://root:password@amiami_mysql_amiami_1/{db}'
        self.db_connection = create_engine(self.db_connection_str)
        self.session = Session(bind=self.db_connection)
        self.create_tables()

    def run_pruebas(self):
        # figure = Figure('Arroz', 'Arroz', 1.25, 'Arroz')
        # db.session.add(figure)
        # db.session.commit()
        # consulta = db.session.query(Figure).get(1)
        d = {
            'name': ['Arroz', 'pollo', 'ostias'],
            'image': ['Arroz', 'pollo', 'ostias'],
            'price': ['Arroz', 'pollo', 'ostias'],
            'brand': ['Arroz', 'pollo', 'ostias'],
            }
        d = {'name': ['New Dimension Game Neptunia VII - Next Purple Processor Unit Full Ver. 1/7 Complete Figure'], 
            'image': ['https://img.amiami.com/images/product/main/182/FIGURE-039829.jpg'],
            'price': ['26,980'],
            'brand': ['Vertex']}
        df = pd.DataFrame(data=d)
        self.clean_table()
        # print(c)
        self.insert_df(df)

    def run_pruebas_multiple(self):
        data = [
                Figure('Arroz', 'pollo', 'leches', 'aria' ), 
                Figure('Arroz', 'pollo', 'leches', 'aria' ), 
                Figure('Arroz', 'pollo', 'leches', 'aria' ), 
            ]
        self.insert_multiple(data)

    def insert_df(self, df):
        i = df.to_sql(self.table_name, con=self.db_connection_str, if_exists='append', index=False)
        print(i)    

    def insert_multiple(self, data):
        self.session.add_all(data)
        self.session.flush()
        self.session.commit()

    def get_all(self):
        return self.session.query(self.model).all()

    def get_all_df(self):
        query = f'SELECT * FROM {self.table_name}'
        df = pd.read_sql(query, con=self.db_connection)
        return df

    def clean_table(self):
        a = db.session.query(self.model).delete()
        print(a)

    def create_tables(self):
        db.Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    got = DatabaseManager('figures')
    got.clean_table()
    got.create_tables()
    # got.get_all_df()