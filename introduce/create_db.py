import pymysql

#MySQL 접속
my_db=pymysql.connect(host='localhost', user='xxxxxx', passwd='xxxxxxx', db='users', charset='utf8')
print(my_db)

#userDB 이용
cursor=my_db.cursor()
cursor.execute('USE users;')

#INSERT문
#cursor.execute('INSERT INTO usertbl (email, age, sex, college_of, how_eat) VALUES ("konkuk@konkuk.ac.kr", 22, "M", "경영대", "기숙사 식당");')

#SELECT문
cursor=my_db.cursor(pymysql.cursors.DictCursor)

cursor.execute('SELECT * FROM usertbl;')
value=cursor.fetchall()
print(value)

#MySQL 접속 종료
my_db.commit()
my_db.close()
