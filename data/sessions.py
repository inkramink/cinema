import sqlalchemy
from .db_session import SqlAlchemyBase


class Sessions(SqlAlchemyBase):
    __tablename__ = 'sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    hall = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    places = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    def __repr__(self):
        return f'<Session> {self.hall} {self.name} {self.time}'
