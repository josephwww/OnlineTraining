import os

from flask import render_template, send_from_directory, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from Course import app, db, bcrypt, qrcode
from Course.forms import LoginForm, CompanyRegistrationForm, UserRegistrationForm, QuestionForm, ClassForm
from Course.models import User, Question, Clas, UserClas, Company
import random


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
    c = Clas.query.filter_by(company_id=current_user.company_id)
    mental = c.filter_by(category='Mental').all()
    physical = c.filter_by(category='Physical').all()
    verbal = c.filter_by(category='Verbal').all()
    if current_user.role == 'admin':
        return redirect(url_for('admin'))
    return render_template('home.html', c=[mental, physical, verbal])


@app.route('/class')
@login_required
def classs():
    records = current_user.clases
    return render_template('class.html', title='Class', classes=records)


@app.route('/intro/<int:class_id>', methods=['GET', 'POST'])
@login_required
def intro(class_id):
    course = Clas.query.filter_by(id=class_id).first()
    mark = -1
    enrolled = False

    for c in course.users:
        if c.user_id == current_user.id:
            enrolled = True
            mark = c.mark
    return render_template(
        'intro.html',
        c=course,
        enrolled=enrolled,
        mark=mark,
        courses=Clas.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if user.username == 'super_admin':
                    return redirect(url_for('super_admin'))
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check your password', 'danger')
        flash('Login Unsuccessful. Username does not exist', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(
            app.root_path,
            'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


@app.route("/class/<int:class_id>", methods=['GET'])
@login_required
def get_class(class_id):
    c = Clas.query.get_or_404(class_id)
    enrolled = False
    for user_class in c.users:
        if current_user.id == user_class.user_id:
            enrolled = True
    if not enrolled:
        user = User.query.filter_by(id=current_user.id).first()
        enroll = UserClas(mark=0, user=user)
        c.users.append(enroll)
        db.session.commit()
        flash(
            f'You have been successfully enrolled in {c.description}',
            'success')
    return render_template('video.html', title='Class', c=c)


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.filter_by(company_id=current_user.company_id).all()
    form = UserRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')
        user = User(
            username=form.username.data,
            password=hashed_password,
            role='student',
            company_id=current_user.company_id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template(
        'user_admin.html',
        title='admin',
        form=form,
        users=users)


@app.route("/test_admin", methods=['GET', 'POST'])
@login_required
def test_admin():
    if current_user.role != 'admin':
        abort(403)
    tests = Clas.query.filter_by(company_id=current_user.company_id).all()
    form = ClassForm()
    if form.validate_on_submit():
        c = Clas(
            category=form.category.data,
            description=form.description.data,
            introduction=form.introduction.data,
            content=form.content.data,
            outcome=form.outcome.data,
            lecturer=form.lecturer.data,
            share=form.share.data,
            video_link=form.video_link.data,
            limit_time=30,
            company_id=current_user.company_id)
        db.session.add(c)
        db.session.commit()
        return redirect(url_for('test_admin'))
    return render_template(
        'test_admin.html',
        title='admin',
        tests=tests,
        form=form)


@app.route("/test", methods=['POST', 'GET'])
@login_required
def exam():
    class_id = request.args.get('class_id', default=1, type=int)
    typ = request.args.get('type', default='', type=str)
    current_year = 2021
    current_semester = 2
    q = Question.query.filter_by(
        clas_id=class_id,
        year=current_year,
        semester=current_semester).all()[:5]
    time_limit = Clas.query.filter_by(id=class_id).first().limit_time
    if typ == 'mock':
        q = Question.query.filter_by(clas_id=class_id).filter(
            Question.year != current_year and Question.semester != current_semester).all()
        # q = random.choices(q, k=5)
        q = q[:5]
    return render_template(
        'test.html',
        title='Test',
        q=q,
        class_id=class_id,
        type=typ,
        time=time_limit)


@app.route("/super_admin", methods=['GET', 'POST'])
@login_required
def super_admin():
    c = Company.query.all()
    if current_user.username != 'super_admin':
        abort(403)
    form = CompanyRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf8')
        company = Company(name=form.username.data)
        db.session.add(company)
        db.session.commit()
        company_id = Company.query.filter_by(
            name=form.username.data).first().id
        user = User(
            username=form.username.data,
            password=hashed_password,
            role='admin',
            company_id=company_id)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('logout'))
    return render_template('register.html', title='Register', form=form, c=c)


@app.route("/change_time/<int:clas_id>/<int:minutes>", methods=['GET', 'POST'])
def change_time(clas_id, minutes):
    course = Clas.query.get_or_404(clas_id)
    if current_user.role != 'admin':
        abort(403)
    course.limit_time = minutes
    db.session.commit()
    return redirect(url_for('test_admin'))


@app.route("/qrcode_login")
def qrcode_login():
    abort(401)


@app.route("/question_admin", methods=['GET', 'POST'])
def question_admin():
    if current_user.role != 'admin':
        abort(403)
    clas_id = request.args.get('class_id', default=-1, type=int)
    semester = request.args.get('semester', default=-1, type=int)
    year = request.args.get('year', default=-1, type=int)
    questions = Question.query
    if clas_id != -1:
        questions = questions.filter_by(clas_id=clas_id)
    if year != -1:
        questions = questions.filter_by(year=year)
    if semester != -1:
        questions = questions.filter_by(semester=semester)

    questions = questions.all()
    form = QuestionForm()
    form.course.choices = list(
        map(lambda x: (x.id, x.description), current_user.owner.clases))
    if form.validate_on_submit():
        q = Question(
            question_type=form.question_type.data,
            year=form.year.data,
            semester=form.semester.data,
            question_text=form.question_text.data,
            clas_id=form.course.data)
        db.session.add(q)
        db.session.commit()
        flash('Question Added', 'success')
        return redirect(
            url_for(
                'question_admin',
                class_id=clas_id,
                year=year,
                semester=semester))
    return render_template(
        'question_admin.html',
        title='admin',
        form=form,
        questions=questions,
        dyear=year,
        dsemester=semester,
        dclas_id=clas_id,
        Q=Question)


@app.route('/finish_course/<int:student_id>/<int:course_id>')
@login_required
def finish_course(student_id, course_id):
    user_class = UserClas.query.filter_by(
        user_id=student_id, clas_id=course_id).first()
    user_class.mark = random.randint(60, 100)
    db.session.commit()
    return redirect(url_for('classs'))
