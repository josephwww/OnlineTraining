from Course import db, bcrypt
from Course.models import User, Question, Clas

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
super_admin = User(username='super_admin', password=hashed_password, company='Admin of', role='super_admin')
test_admin = User(username='test', password=hashed_password, company='example_company', role='admin')
test_student = User(username='student', password=hashed_password, company='example_company', role='student')
test_class = Clas(description='Being Assertive', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='N/A', video_link='https://www.youtube.com/embed/NBkvWCmz2W4', limit_time=30)
test_class1 = Clas(description='Communicating Non-Verbally', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='N/A', video_link='https://www.youtube.com/embed/fLaslONQAKM', limit_time=30)
test_class2 = Clas(description='Communicating Verbally', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='Achieved', video_link='https://www.youtube.com/embed/wOhLMEKLTKE', limit_time=30)
test_class3 = Clas(description='Preparing Introduction', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='N/A', video_link='https://www.youtube.com/embed/QgjkjsqAzvo', limit_time=30)
test_class4 = Clas(description='Practicing Active Listening', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='N/A', video_link='https://www.youtube.com/embed/7wUCyjiyXdg', limit_time=30)
test_class5 = Clas(description='Overcoming Telephone Phobia', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='N/A', video_link='https://www.youtube.com/embed/jeUovnNp3Yk', limit_time=30)
test_class6 = Clas(description='Accepting and Giving Compliments', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='Achieved', video_link='https://www.youtube.com/embed/_EKXNmM1PUo', limit_time=30)
test_class7 = Clas(description='Custom Made Individual or Group Training', introduction='N/A', content='N/A', outcome='N/A', lecturer='N/A', share='N/A', recipe='N/A', video_link='https://www.youtube.com/embed/xojGj9_BpKM', limit_time=30)



db.session.add(test_class)
db.session.add(test_class1)
db.session.add(test_class2)
db.session.add(test_class3)
db.session.add(test_class4)
db.session.add(test_class5)
db.session.add(test_class6)
db.session.add(test_class7)
db.session.add(super_admin)
db.session.add(test_admin)
db.session.add(test_student)

db.session.commit()

qt = {'YN': 'Yes/No', 'MC': 'Multiple Choice', 'ET': 'Essay Type', "C": "Comprehensive"}
for course in Clas.query.all():
    for year in range(2010, 2022):
        for semester in range(1,3):
            for question_type in ('YN', 'MC', 'ET', 'C'):
                q = Question(question_type=question_type, year=year, semester=semester, question_text=f'Example Question for Course {course.description} in year {year} S{semester} with Question Type {qt[question_type]}', clas_id=course.id)
                db.session.add(q)
db.session.commit()