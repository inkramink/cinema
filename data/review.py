import sqlalchemy
from .db_session import SqlAlchemyBase


class Review(SqlAlchemyBase):
    __tablename__ = 'comms'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    film_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
