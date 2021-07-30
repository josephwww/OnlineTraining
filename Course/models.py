# define the database
from datetime import datetime
from Course import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

question_test_association_table = db.Table('question_test',
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'), primary_key=True),
    db.Column('test_id', db.Integer, db.ForeignKey('test.id'), primary_key=True)
)

user_class_association_table = db.Table('user_class',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True)
)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    company = db.Column(db.String(60), nullable=True)
    role = db.Column(db.String(10), nullable=False)
    classes = db.relationship('Class', secondary=user_class_association_table, lazy='subquery', backref=db.backref('stus', lazy=True))
    tests = db.relationship('Test', backref='tester', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.company}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.String(200), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    tests = db.relationship('Test', secondary=question_test_association_table, lazy='subquery', backref=db.backref('qs', lazy=True))

    def __repr__(self):
        return f"Question('{self.question}' in year {self.year} semester {self.semester})"


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    mark = db.Column(db.Integer, nullable=True)
    time_limit = db.Column(db.Integer, nullable=False)

    questions = db.relationship('Question', secondary=question_test_association_table, lazy='subquery', backref=db.backref('ts', lazy=True))

    def __repr__(self):
        return f"Test('{self.tester} ,mark{self.mark}, time_limit{self.time_limit})"


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=True)
    introduction = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(200), nullable=True)
    outcome = db.Column(db.String(200), nullable=True)
    lecturer = db.Column(db.String(200), nullable=True)
    share = db.Column(db.String(200), nullable=True)
    recipe = db.Column(db.String(200), nullable=True)

    questions = db.relationship('Question', backref='questions', lazy='dynamic')
    students = db.relationship('User', secondary=user_class_association_table, lazy='subquery', backref=db.backref('courses', lazy=True))

    def __repr__(self):
        return f"Class {self.description}"

