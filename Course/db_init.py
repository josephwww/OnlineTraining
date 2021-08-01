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
test_class = Class(description='COMP1234', introduction='Computer Network', content='OSM Seven Layers', outcome='example', lecturer='Joseph', share='example', recipe='NA')
test_class1 = Class(description='COMP1234', introduction='Operation System', content='C Language', outcome='example', lecturer='Joseph', share='example', recipe='NA')
test_class2 = Class(description='COMP2341', introduction='Data Warehouse', content='SQL', outcome='example', lecturer='Joseph', share='example', recipe='Achieved')
test_class3 = Class(description='COMP3412', introduction='Software Engineering', content='Design Pattern', outcome='example', lecturer='Joseph', share='example', recipe='NA')

test_class.students.append(test_student)
test_class1.students.append(test_student)
test_class2.students.append(test_student)
test_class3.students.append(test_student)

db.session.add(test_class)
db.session.add(test_class1)
db.session.add(test_class2)
db.session.add(test_class3)

db.session.add(test_admin)
db.session.add(test_student)

db.session.commit()
