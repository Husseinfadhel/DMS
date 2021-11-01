from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


class Users(db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(Integer)
    auth = Column(Integer)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Client(db.Model):
    __tablename__ = "Client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone = Column(Integer)
    address = Column(String)
    order = db.relationship('Orders', backref=db.backref('client', uselist=False), lazy='dynamic')

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            "phone": self.phone
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Masareef(db.Model):
    __tablename__ = "Masareef"
    id = Column(Integer, primary_key=True)
    reason = Column(String)
    amount = Column(Integer)
    date = Column(String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Driver(db.Model):
    __tablename__ = "Driver"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(Integer)
    card_no = Column(Integer)
    order = db.relationship('Orders', backref=db.backref('driver', uselist=False), lazy='dynamic')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Orders(db.Model):
    __tablename__ = "Orders"
    id = Column(Integer, primary_key=True)
    invoice_num = Column(Integer)
    client_id = Column(Integer, ForeignKey('Client.id'))
    date = Column(String)
    total_cost = Column(Integer)
    net_cost = Column(Integer)
    driver_id = Column(Integer, ForeignKey('Driver.id'))
    state = Column(Integer, default=0)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
