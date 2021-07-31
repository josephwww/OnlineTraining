from Course import db, bcrypt
from Course.models import User, Question, Test, Class

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
test_admin = User(username='test', password=hashed_password, company='example_company', role='admin')
test_student = User(username='student', password=hashed_password, company='example_company', role='student')
db.session.add(test_admin)
db.session.add(test_student)
db.session.commit()
