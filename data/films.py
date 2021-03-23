import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase, UserMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    length = sqlalchemy.Column(sqlalchemy.Integer, default=120)
    image_route = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    age_restriction = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='Film')

    def __repr__(self):
        return f'<Film> {self.id} {self.name}'
