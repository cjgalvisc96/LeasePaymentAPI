from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModelMixin:

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as error:
            raise error

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def simple_filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
