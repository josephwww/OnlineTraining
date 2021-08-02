from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NoneOf, NumberRange
from Course.models import User, Clas

'''
setting the form in the application 
'''
class CompanyRegistrationForm(FlaskForm):
    username = StringField('Company Name', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmed Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add Company')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmed Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class QuestionForm(FlaskForm):
    question_type = SelectField('Question Type', choices=[('YN', 'Yes/No'), ('MC', 'Multiple Choice'), ('ET', 'Essay Type'), ('C', 'Comprehensive')], validators=[])
    question_text = StringField('Question', validators=[DataRequired()])
    year = IntegerField('Year', validators=[])
    semester = SelectField('Semester', choices=[(1, 1), (2,2)], validators=[DataRequired()], coerce=int)
    course = SelectField('Course', choices=Clas.query.with_entities(Clas.id, Clas.description).all(), validators=[], coerce=int)
    submit = SubmitField('Add Question')