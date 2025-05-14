import sqlalchemy
from .db_session import SqlAlchemyBase


class Sponsor(SqlAlchemyBase):
    __tablename__ = 'sponsors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # id
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Название спонсора
    information = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Информация о спонсоре в виде строки
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # Путь до файла с изображением
