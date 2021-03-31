import sqlalchemy
from .db_session import SqlAlchemyBase


class Hall(SqlAlchemyBase):
    __tablename__ = 'halls'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    rows = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    columns = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
