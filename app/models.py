from app import db, engine
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy import MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)
metadata = MetaData(bind=engine)

from app import app, engine
from sqlalchemy.orm import Session
session = Session(engine)

class Users(UserMixin, Base):
    __table__ = Table('users', metadata, autoload=True)

    # id = db.Column(db.String, primary_key=True)
    # UserName = db.Column(db.String)
    # email = db.Column(db.String)
    # password_hash = db.Column(db.String)

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        if self.PasswordHash is not None:
            return check_password_hash(self.PasswordHash, password)
        else:
            return False

    def get_id(self):
        return self.ID

    def __repr__(self):
        return '<User {}>'.format(self.UserName)

@login.user_loader
def load_user(id):
    return session.query(Users).get(id)