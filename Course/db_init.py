from Course import db, bcrypt
from Course.models import User, Question, Clas, Company

'''
This script initialises the database and create an admin account for the application
'''

db.create_all()
# insert all the movies to the database
# for movie_id, movie_name in get_movies():
#     movie = Movie(id=movie_id, name=movie_name)
#     db.session.add(movie)

# create an admin account
hashed_password = bcrypt.generate_password_hash('test').decode('utf8')
roles = {'admin': 'admin', 'student': 'student'}
company = Company(name='example')
db.session.add(company)
db.session.commit()
company_id = Company.query.first().id
super_admin = User(username='super_admin', password=hashed_password, role='super_admin',  company_id=company_id)
test_admin = User(username='test', password=hashed_password, role='admin', company_id=company_id)
test_student = User(username='student', password=hashed_password, role='student', company_id=company_id)



db.session.add(super_admin)
db.session.add(test_admin)
db.session.add(test_student)

db.session.commit()

# qt = {'YN': 'Yes/No', 'MC': 'Multiple Choice', 'ET': 'Essay Type', "C": "Comprehensive"}
# for course in Clas.query.all():
#     for year in range(2010, 2022):
#         for semester in range(1,3):
#             for question_type in ('YN', 'MC', 'ET', 'C'):
#                 q = Question(question_type=question_type, year=year, semester=semester, question_text=f'Example Question for Course {course.description} in year {year} S{semester} with Question Type {qt[question_type]}', clas_id=course.id)
#                 db.session.add(q)
# db.session.commit()