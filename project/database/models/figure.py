from .. import db
from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

class Figure(db.Base):
    __tablename__ = 'figure'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    image = Column(String(256), nullable=False)
    price = Column(String(256), nullable=False)
    brand = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False)

    def __init__(self, name, image, price, brand, url):
        self.name = name
        self.image = image
        self.price = price
        self.brand = brand
        self.url = url

    def __repr__(self):
        return f'Figura({self.name}, {self.price}, {self.price})'
    def __str__(self):
        return f'Figura({self.name}, {self.image}, {self.price}, {self.brand})'