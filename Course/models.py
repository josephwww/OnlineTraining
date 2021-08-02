# define the database
from datetime import datetime
from Course import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# question_test_association_table = db.Table('question_test',
#     db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
#     db.Column('test_id', db.Integer, db.ForeignKey('test.id'), primary_key=True)
# )

# user_class_association_table = db.Table('user_class',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
#     db.Column('mark', db.Integer),
#     db.relationship('User', backref='user_class')
# )

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
    company = db.Column(db.String(60), nullable=True)
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

    # tests = db.relationship('Test', secondary=question_test_association_table, lazy='subquery', backref=db.backref('qs', lazy=True))

    def __repr__(self):
        return f"Question('{self.question_type}' in year {self.year} semester {self.semester})"


class Clas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=True)
    introduction = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(200), nullable=True)
    outcome = db.Column(db.String(200), nullable=True)
    lecturer = db.Column(db.String(200), nullable=True)
    share = db.Column(db.String(200), nullable=True)
    recipe = db.Column(db.String(200), nullable=True)
    video_link = db.Column(db.String(500), nullable=False)
    limit_time = db.Column(db.Integer, nullable=False)

    questions = db.relationship('Question', backref='course', lazy='dynamic')
    # students = db.relationship('User', secondary=user_class_association_table, lazy='subquery', backref=db.backref('courses', lazy=True))
    users = db.relationship('UserClas', back_populates='clas')

    def __repr__(self):
        return f"Clas {self.description}"

