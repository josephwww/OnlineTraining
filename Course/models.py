# define the database
from datetime import datetime
from Course import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    users = db.relationship('User', backref='owner', lazy='dynamic')
    clases = db.relationship('Clas', backref='company', lazy='dynamic')


class UserClas(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    clas_id = db.Column(db.Integer, db.ForeignKey('clas.id'), primary_key=True)
    mark = db.Column(db.Integer)
    clas = db.relationship('Clas', back_populates='users')
    user = db.relationship('User', back_populates='clases')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    role = db.Column(db.String(10), nullable=False)

    clases = db.relationship('UserClas', back_populates='user')

    def __repr__(self):
        return f"User('{self.username}', Company: '{self.company}', Role: {self.role})"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.String(200), nullable=False)
    clas_id = db.Column(db.Integer, db.ForeignKey('clas.id'))


    def __repr__(self):
        return f"Question('{self.question_type}' in year {self.year} semester {self.semester})"


class Clas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    introduction = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(200), nullable=True)
    outcome = db.Column(db.String(200), nullable=True)
    lecturer = db.Column(db.String(200), nullable=True)
    share = db.Column(db.String(200), nullable=True)
    recipe = db.Column(db.String(200), nullable=True)
    video_link = db.Column(db.String(500), nullable=False)
    limit_time = db.Column(db.Integer, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    questions = db.relationship('Question', backref='course', lazy='dynamic')
    users = db.relationship('UserClas', back_populates='clas')

    def __repr__(self):
        return f"Clas {self.description}"
