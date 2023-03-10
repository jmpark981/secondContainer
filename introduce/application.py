from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, IntegerField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired
from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
import sys


app = Flask(__name__)      # 서버 생성
csrf = CSRFProtect(app)    # form이 제대로 전송되었는지 확인

#데이터 베이스 추가
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://joonmo:os2window@localhost/users"

#폼 비밀키 설정
app.config['SECRET_KEY']="my super secret key"


#Initalize DB
db=SQLAlchemy(app)

#모델 생성 -> table 생성
class Usertbl(db.Model):
    __table_name__ = 'usertbl'
    
    email=db.Column(db.String(30), primary_key=True)
    sex=db.Column(db.String(5), nullable=False)
    age=db.Column(db.Integer, nullable=False)
    dorm_select=db.Column(db.String(10), nullable=False)
    
    college_of=db.Column(db.String(30), nullable=False)
    personality=db.Column(db.String(5), nullable=False)
    weekend_stay=db.Column(db.String(5), nullable=False)
    weekday_stay=db.Column(db.String(30), nullable=False)
    smoke=db.Column(db.String(5), nullable=False)
    alcohol=db.Column(db.String(5), nullable=False)
    how_eat=db.Column(db.String(45), nullable=False)
    how_eat_in=db.Column(db.String(5), nullable=False)
    wake_up=db.Column(db.String(10), nullable=False)
    sleep=db.Column(db.String(5), nullable=False)
    sleep_sensitive=db.Column(db.String(10), nullable=False)
    sleep_habit=db.Column(db.String(5), nullable=False)
    clean_period=db.Column(db.String(10), nullable=False)
    shower_timezone=db.Column(db.String(5), nullable=False)
    

#멀티 체크박스 필드 생성
class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


#폼 클래스 만들기
class BaseForm(FlaskForm):
    #설문지
    personality=RadioField("6. 성격 유형", choices=[('E','외향적'),('I','내향적')], validators=[InputRequired()])
    weekend_stay=RadioField("7. 주말 거주 유형", choices=[('주로 기숙사내','주로 기숙사내'),('주로 기숙사 밖','주로 기숙사 밖')], validators=[InputRequired()])
    weekday_stay=RadioField("8. 평일 거주 유형", choices=[('아침', '아침'), ('점심', '점심'), ('저녁', '저녁')])
    smoke=RadioField("9. 흡연 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    alcohol=RadioField("10. 음주 정도", choices=[('자주', '자주'), ('보통', '보통'), ('드물게', '드물게')])
    how_eat=RadioField("11. 식사 해결 장소", choices=[('기숙사 내', '기숙사 내'), ('기숙사 밖', '기숙사 밖'), ('기숙사 식당', '기숙사 식당')])
    how_eat_in=RadioField("12. 배달음식 같이 먹기 희망 여부", choices=[('Y','매우 희망'),('N','비희망')], validators=[InputRequired()])
    wake_up=RadioField("13. 평균 기상 시간", choices=[('6시~8시','6시~8시'),('8시~10시','8시~10시'),('10시~12시','10시~12시'), ('12시이후','12시 이후')], validators=[InputRequired()])
    sleep=RadioField("14. 평균 취침 시간", choices=[('10시~12시','10시~12시'),('12시~2시','12시~2시'),('2시 이후','새벽')], validators=[InputRequired()])
    sleep_sensitive=RadioField("15. 취침시 예민도", choices=[('예민','예민'),('둔감','둔감')], validators=[InputRequired()])
    sleep_habit=RadioField("16. 잠버릇 유무", choices=[('있다','그렇다'), ('보통', '보통'), ('없다','없다')], validators=[InputRequired()])
    clean_period=RadioField("17. 일주일동안 청소 빈도", choices=[('자주(5회~7회)','자주(5회~7회)'),('보통(2회~4회)','보통(2회~4회)'),('드물게(1회~0회)','드물게(1회~0회)')], validators=[InputRequired()])
    shower_timezone=RadioField("18. 샤워 시간대", choices=[('아침','아침'),('저녁','저녁')], validators=[InputRequired()])
    
    submit=SubmitField("다음 페이지로")

class UserForm(BaseForm):
    #유저 정보
    email=StringField("1.이메일", validators=[InputRequired()])
    age=IntegerField("2. 나이", validators=[InputRequired()])
    sex=RadioField("3. 성별", choices=[('M','남자'),('W','여자')], validators=[InputRequired()])
    dorm_select=RadioField("4. 거주 홀 정보", choices=[('레이크', '레이크홀'), ('비레이크', '비레이크홀')])
    college_of=SelectField("5. 단과대", choices=[('문과대', '문과대'), ('이과대', '이과대'), ('건축대', '건축대'), ('공과대', '공과대'), ('사과대', '사과대'), 
                                              ('경영대', '경영대'), ('부동산대', '부동산대'), ('융기원', '융기원'), ('생명과학대', '생명과학대'), ('수의대', '수의대'),
                                              ('예디대', '예디대'), ('사범대', '사범대'), ('그외', '그외')], validators=[InputRequired()])
    #1: 문과대	2: 이과대	3. 건축대	4. 공과대	5. 사과대	6. 경영대	7. 부동산	8. 융기원	9. 생명과학대 10. 수의대 11. 예디대 12. 사범대 13. 그외
    
class MateForm(BaseForm):
    age_range=MultiCheckBoxField("20. 원하는 룸메 나이대", choices=[('또래', '두 살 차이 내'), ('또래 이상', '두 살 차이 이상')])
    diff_college_of=RadioField("6. 소속이 다른 사람 원하는 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    submit=SubmitField("Submit")
    
@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/servey", methods=["GET", "POST"])
def servey():
    email, sex, age, dorm_select, college_of, personality, weekend_stay, weekday_stay=None, 0, None, None, None, None, None, None
    smoke, alcohol, how_eat, how_eat_in, wake_up, sleep, sleep_sensitive, sleep_habit, clean_period=None, None, None, None, None, None, None, None, None
    shower_timezone=None
    error_msg=""
    form=UserForm(request.form)
    
    kwargs={'email': email, 'sex': sex, 'age': age, 'dorm_select': dorm_select, 'college_of': college_of, 'personality': personality,
            'weekend_stay': weekend_stay, 'weekday_stay': weekday_stay, 'smoke': smoke, 'alcohol': alcohol, 'how_eat': how_eat, 'how_eat_in': how_eat_in, 'wake_up': wake_up,
            'sleep': sleep, 'sleep_sensitive': sleep_sensitive, 'sleep_habit': sleep_habit, 'clean_period': clean_period, 
            'shower_timezone': shower_timezone}
    
    #Validate Form 입력 완료 후 받은 데이터 저장
    if request.method=="POST" and form.validate():
        print(form.email.data)
        before_mail=form.email.data
        existingEmail=Usertbl.query.filter_by(email=form.email.data).first()
        print(existingEmail)
        
        #해당 이메일을 가진 유저가 존재한다면 (이메일 중복 방지) 아니면 DB에 추가
        if existingEmail is not None:
            form=UserForm(formdata=None)
            error_msg="중복되는 이메일"
            return render_template("servey.html", error_msg=error_msg, **kwargs, form=form)
        else:   # 데이터 입력 되는 부분
            user=Usertbl(email=form.email.data, sex=form.sex.data, age=form.age.data, dorm_select = form.dorm_select.data ,
                        college_of=form.college_of.data, personality = form.personality.data, weekend_stay=form.weekend_stay.data, 
                        weekday_stay=form.weekday_stay.data, smoke=form.smoke.data, alcohol=form.alcohol.data, how_eat=form.how_eat.data, 
                        how_eat_in=form.how_eat_in.data, wake_up=form.wake_up.data, sleep=form.sleep.data, sleep_sensitive=form.sleep_sensitive.data,
                        sleep_habit=form.sleep_habit.data, clean_period=form.clean_period.data, shower_timezone=form.shower_timezone.data)
            
            db.session.add(user)
            db.session.commit()
            #my_dic = {''}
            return redirect(url_for('servey2'))
        
        #Clear Form
        form=UserForm(formdata=None)
    
    return render_template("servey.html", error_msg=error_msg, **kwargs, form=form)


@app.route("/servey2", methods=["GET", "POST"])
def servey2():
    age_range, diff_college_of, personality, weekend_stay, weekday_stay=None, None, None, None, None
    smoke, alcohol, how_eat, how_eat_in, wake_up, sleep, sleep_sensitive, sleep_habit, clean_period=None, None, None, None, None, None, None, None, None
    shower_time, shower_timezone, material_share, bug_catch, phone_chat_in, phone_chat_time, age_range=None, None, None, None, None, None, None
    dorm_select=None
    error_msg=""
    form=MateForm(request.form)
    
    kwargs={'age_range': age_range, 'diff_college_of': diff_college_of, 'personality': personality, 'weekend_stay': weekend_stay, 
            'weekday_stay': weekday_stay, 'smoke': smoke, 'alcohol': alcohol, 'how_eat': how_eat, 'how_eat_in': how_eat_in, 'wake_up': wake_up,
            'sleep': sleep, 'sleep_sensitive': sleep_sensitive, 'sleep_habit': sleep_habit, 'clean_period': clean_period, 
            'shower_timezone': shower_timezone}
    
    #Validate Form
    if request.method=="POST":
        print('성공적1')
        if form.validate():
            print('성공적')
            user_dict={'age_range': form.age_range.data, 'diff_college_of': form.diff_college_of.data, 'personality': form.personality.data, 
                       'weekend_stay': form.weekend_stay.data, 'weekday_stay': form.weekday_stay.data, 'smoke': form.smoke.data, 'alcohol': form.alcohol.data, 
                       'how_eat': form.how_eat.data, 'how_eat_in': form.how_eat_in.data, 'wake_up': form.wake_up.data, 'sleep': form.sleep.data, 
                       'sleep_sensitive': form.sleep_sensitive.data, 'sleep_habit': form.sleep_habit.data, 'clean_period': form.clean_period.data, 
                       'shower_timezone': form.shower_timezone.data }


            return redirect(url_for('qna', user_dict=user_dict), code=307)
        
    #Clear Form
    print('실패') 
    print(form.errors)
    form=MateForm(formdata=None)
    
    return render_template("servey2.html", error_msg=error_msg, **kwargs, form=form)


@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/qna<user_dict>", methods=["GET", "POST"])
def qna(user_dict):
    #mate_info=request.form.get("user_dict")
    show_users=Usertbl.query.all()
    return render_template("qna.html", user_dict=user_dict, show_users=show_users)

@app.route("/creator")
def creator():
    return render_template("creator.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
