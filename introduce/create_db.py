import pymysql

#MySQL 접속
my_db=pymysql.connect(host='localhost', user='joonmo', passwd='os2window', db='users', charset='utf8')
print(my_db)

#userDB 이용
cursor=my_db.cursor()
cursor.execute('USE users;')

#INSERT문
#cursor.execute('INSERT INTO usertbl (email, age, sex, college_of, how_eat) VALUES ("konkuk@konkuk.ac.kr", 22, "M", "경영대", "기숙사 식당");')

#temp
# email=db.Column(db.String(30), primary_key=True)
#     sex=db.Column(db.String(5), nullable=False)
#     age=db.Column(db.Integer, nullable=False)
#     dorm_select=db.Column(db.String(10), nullable=False)
    
#     college_of=db.Column(db.String(30), nullable=False)
#     personality=db.Column(db.String(5), nullable=False)
#     weekend_stay=db.Column(db.String(5), nullable=False)
#     weekday_stay=db.Column(db.String(30), nullable=False)
#     smoke=db.Column(db.String(5), nullable=False)
#     alcohol=db.Column(db.String(5), nullable=False)
#     how_eat=db.Column(db.String(45), nullable=False)
#     how_eat_in=db.Column(db.String(5), nullable=False)
#     wake_up=db.Column(db.String(10), nullable=False)
#     sleep=db.Column(db.String(5), nullable=False)
#     sleep_sensitive=db.Column(db.String(10), nullable=False)
#     sleep_habit=db.Column(db.String(5), nullable=False)
#     clean_period=db.Column(db.String(10), nullable=False)
#     shower_timezone=db.Column(db.String(5), nullable=False)
sql="""
    CREATE TABLE usertbl(
    email VARCHAR(30) PRIMARY KEY,
    sex VARCHAR(5) NOT NULL,
    age INT NOT NULL,
    dorm_select VARCHAR(10) NOT NULL,
    college_of VARCHAR(30) NOT NULL,
    personality VARCHAR(5) NOT NULL,
    weekend_stay VARCHAR(5) NOT NULL,
    weekday_stay VARCHAR(30) NOT NULL,
    smoke VARCHAR(5) NOT NULL,
    alcohol VARCHAR(5) NOT NULL,
    how_eat VARCHAR(45) NOT NULL,
    how_eat_in VARCHAR(5) NOT NULL,
    wake_up VARCHAR(10) NOT NULL,
    sleep VARCHAR(5) NOT NULL,
    sleep_sensitive VARCHAR(10) NOT NULL,
    sleep_habit VARCHAR(5) NOT NULL,
    clean_period VARCHAR(10) NOT NULL,
    shower_timezone VARCHAR(5) NOT NULL
    );
"""
cursor.execute(sql)
my_db.commit()
my_db.close()
# #SELECT문
# cursor=my_db.cursor(pymysql.cursors.DictCursor)

# cursor.execute('SELECT * FROM usertbl;')
# value=cursor.fetchall()
# print(value)

# #MySQL 접속 종료
# my_db.commit()
# my_db.close()
