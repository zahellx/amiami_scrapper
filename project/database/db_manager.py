from .models.figure import Figure
from sqlalchemy import create_engine
import pandas as pd
from . import db

# Este proyecto va a hacer las peticiones directamente con pd porque es mas eficiente, asi probamos tambien sql con pandas
class DatabaseManager():
    def __init__(self, model):
        db = 'db'
        self.table_name = model.__tablename__
        self.db_connection_str = f'mysql+pymysql://user:password@amiami_mysql_amiami_1/{db}'
        self.db_connection = create_engine(self.db_connection_str)

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
        df = pd.DataFrame(data=d)
        df.to_sql(self.table_name, con=self.db_connection_str, if_exists='append', index=False)

    def insert_df(self, df):
        df.to_sql(self.table_name, con=self.db_connection_str, if_exists='append', index=False)

    def get_all_df(self):
        query = f'SELECT * FROM {self.table_name}'
        df = pd.read_sql(query, con=self.db_connection)
        return df

    def clean_table(self):
        db.session.query(Figure).delete()

    def create_tables(self):
        db.Base.metadata.create_all(db.engine)


if __name__ == "__main__":
    got = DatabaseManager('figures')
    got.create_tables()
    # got.get_all_df()