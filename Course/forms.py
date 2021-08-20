from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NoneOf, NumberRange
from Course.models import User, Clas

'''
setting the form in the application 
'''
class CompanyRegistrationForm(FlaskForm):
    username = StringField('Company Name', validators=[DataRequired()])
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

class ClassForm(FlaskForm):
    category = SelectField('Category', choices=[('Mental', 'Mental'), ('Physical', 'Physical'), ('Verbal', 'Verbal')], validators=[DataRequired()], coerce=str)
    description = StringField('Description', validators=[DataRequired()])
    introduction = StringField('Introduction', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    outcome = StringField('Outcome', validators=[DataRequired()])
    lecturer = StringField('Lecturer', validators=[DataRequired()])
    share = StringField('Share', validators=[DataRequired()])
    video_link = StringField('Video link', validators=[DataRequired()])
    submit = SubmitField('Add Course')

class QuestionForm(FlaskForm):
    question_type = SelectField('Question Type', choices=[('YN', 'Yes/No'), ('MC', 'Multiple Choice'), ('ET', 'Essay Type'), ('C', 'Comprehensive')], validators=[])
    question_text = StringField('Question', validators=[DataRequired()])
    year = IntegerField('Year', validators=[])
    semester = SelectField('Semester', choices=[(1, 1), (2,2)], validators=[DataRequired()], coerce=int)
    course = SelectField('Course', choices=[], validators=[], coerce=int)
    submit = SubmitField('Add Question')