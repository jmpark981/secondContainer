from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, SubmitField, IntegerField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import InputRequired
from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
import sys


app = Flask(__name__)
csrf = CSRFProtect(app)

#데이터 베이스 추가
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://xxxxx:xxxxxx@localhost/users"

#폼 비밀키 설정
app.config['SECRET_KEY']="my super secret key"


#Initalize DB
db=SQLAlchemy(app)

#모델 생성
class Usertbl(db.Model):
    __table_name__ = 'usertbl'
    
    email=db.Column(db.String(30), primary_key=True)
    age=db.Column(db.Integer, nullable=False)
    sex=db.Column(db.String(5), nullable=False)
    college_of=db.Column(db.String(30), nullable=False)
    newbie_in=db.Column(db.String(5), nullable=False)
    diff_college_of=db.Column(db.String(5), nullable=False)
    personality=db.Column(db.String(5), nullable=False)
    weekend_stay=db.Column(db.String(5), nullable=False)
    weekday_stay=db.Column(db.String(30), nullable=False)
    smoke=db.Column(db.String(5), nullable=False)
    alcohol=db.Column(db.String(5), nullable=False)
    how_eat=db.Column(db.String(45), nullable=False)
    how_eat_in=db.Column(db.String(5), nullable=False)
    wake_up=db.Column(db.String(10), nullable=False)
    stay_overnight_test=db.Column(db.String(10), nullable=False)
    sleep=db.Column(db.String(5), nullable=False)
    sleep_habit=db.Column(db.String(5), nullable=False)
    clean_period=db.Column(db.String(10), nullable=False)
    shower_time=db.Column(db.String(10), nullable=False)
    shower_timezone=db.Column(db.String(5), nullable=False)
    material_share=db.Column(db.String(5), nullable=False)
    bug_catch=db.Column(db.String(5), nullable=False)
    phone_chat_in=db.Column(db.String(5), nullable=False)
    phone_chat_time=db.Column(db.String(10), nullable=False)
    age_range=db.Column(db.String(10), nullable=False)


#멀티 체크박스 필드 생성
class MultiCheckBoxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


#폼 클래스 만들기
class UserForm(FlaskForm):
    email=StringField("1.이메일", validators=[InputRequired()])
    age=IntegerField("2. 나이", validators=[InputRequired()])
    sex=RadioField("3. 성별", choices=[('M','남자'),('W','여자')], validators=[InputRequired()])
    college_of=SelectField("4. 단과대", choices=[('경영대', '경영대'), ('사과대', '사과대'), ('예디대', '예디대'), ('공과대', '공과대'), ('융기원', '융기원')], validators=[InputRequired()])
    newbie_in=RadioField("5. 신규입주생", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    diff_college_of=RadioField("6. 소속이 다른 사람 원하는 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    personality=RadioField("7. 성격", choices=[('E','외향적'),('I','내향적')], validators=[InputRequired()])
    
    weekend_stay=RadioField("8-1. 주말 거주 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    weekday_stay=MultiCheckBoxField("8-2. 평일 거주시간", choices=[('아침', '아침'), ('점심', '점심'), ('저녁', '저녁')])
    
    smoke=RadioField("9. 흡연 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    alcohol=RadioField("10. 술 마시는 정도", choices=[('자주', '자주'), ('보통', '보통'), ('드물게', '드물게')])
    how_eat=MultiCheckBoxField("11-1. 식사 해결 방법", choices=[('기숙사 식당', '기숙사 식당'), ('외식', '외식'), ('기숙사 안', '기숙사 안')])
    how_eat_in=RadioField("11-2. 기숙사 안 같이 먹기 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    
    wake_up=RadioField("12. 기상 시간", choices=[('일찍','6시~8시'),('보통','8시~10시'),('늦게','12시 이후')], validators=[InputRequired()])
    
    sleep=RadioField("13-1. 취침 시간", choices=[('일찍','10시~12시'),('보통','12시~2시'),('늦게','새벽')], validators=[InputRequired()])
    stay_overnight_test=RadioField("13-2. 시험 기간 밤샘 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    
    sleep_habit=RadioField("14. 잠버릇 허용 유무", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    clean_period=RadioField("15. 일주일동안 청소 빈도", choices=[('자주','자주(5~7)'),('보통','보통(5~7)'),('드물게','드물게(5~7)')], validators=[InputRequired()])
    
    shower_time=RadioField("16-1. 샤워 시간", choices=[('짧게','0~20분'),('길게','20분 over')], validators=[InputRequired()])
    shower_timezone=RadioField("16-2. 샤워 시간대", choices=[('아침','아침'),('저녁','저녁')], validators=[InputRequired()])
    
    material_share=RadioField("17. 물품 공유 여부", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    bug_catch=RadioField("18. 벌레 잡을 수 있는 지 여부", choices=[('Y','그렇다'),('N','아니다')], validators=[InputRequired()])
    
    phone_chat_in=RadioField("19-1. 전화 통화 여부", choices=[('실내','실내'),('실외','실외')], validators=[InputRequired()])
    phone_chat_time=RadioField("19-2. 하루 평균 통화 시간", choices=[('드물게','20분 미만'),('보통','20분~1시간'),('자주','1시간 이상')], validators=[InputRequired()])
        
    age_range=RadioField("20. 원하는 룸메 나이대", choices=[('또래', '두 살 차이 내'), ('또래 이상', '두 살 차이 이상')])
    submit=SubmitField("Submit")

    
@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/servey", methods=["GET", "POST"])
def servey():
    email, age, sex, college_of, newbie_in, diff_college_of, personality, weekend_stay, weekday_stay=None, 0, None, None, None, None, None, None, None
    smoke, alcohol, how_eat, how_eat_in, wake_up, sleep, stay_overnight_test, sleep_habit, clean_period=None, None, None, None, None, None, None, None, None
    shower_time, shower_timezone, material_share, bug_catch, phone_chat_in, phone_chat_time, age_range=None, None, None, None, None, None, None
    error_msg=""
    form=UserForm(request.form)
    
    kwargs={'email': email, 'age': age, 'college_of': college_of,' newbie_in': newbie_in, 'diff_college_of': diff_college_of, 'personality': personality,
            'weekend_stay': weekend_stay, 'smoke': smoke, 'alcohol': alcohol, 'how_eat': how_eat, 'how_eat_in': how_eat_in, 'wake_up': wake_up,
            'sleep': sleep, 'stay_overnight_test': stay_overnight_test, 'sleep_habit': sleep_habit, 'clean_period': clean_period, 'shower_time': shower_time, 
            'shower_timezone': shower_timezone, 'material_share': material_share, 'bug_catch': bug_catch, 'phone_chat_in': phone_chat_in, 
            'phone_chat_time': phone_chat_time, 'age_range': age_range}
    
    #Validate Form
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
        else:
            user=Usertbl(email=form.email.data, age=form.age.data, sex=form.sex.data, college_of=form.college_of.data, 
                         newbie_in=form.newbie_in.data, diff_college_of=form.diff_college_of.data, personality=form.personality.data, 
                         weekend_stay=form.weekend_stay.data, weekday_stay="&".join(form.weekday_stay.data), smoke=form.smoke.data, alcohol=form.alcohol.data, 
                         how_eat="&".join(form.how_eat.data), how_eat_in=form.how_eat_in.data, wake_up=form.wake_up.data, sleep=form.sleep.data, 
                         stay_overnight_test=form.stay_overnight_test.data, sleep_habit=form.sleep_habit.data, clean_period=form.clean_period.data, 
                         shower_time=form.shower_time.data, shower_timezone=form.shower_timezone.data, material_share=form.material_share.data, 
                         bug_catch=form.bug_catch.data, phone_chat_in=form.phone_chat_in.data, phone_chat_time=form.phone_chat_time.data, 
                         age_range=form.age_range.data)
            
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('qna', email=form.email.data))
        
        #Clear Form
        form=UserForm(formdata=None)
    
    return render_template("servey.html", error_msg=error_msg, **kwargs, form=form)

@app.route("/result")
def result():
    return render_template("result.html")

@app.route("/qna/<email>", methods=["GET", "POST"])
def qna(email):
    show_users=Usertbl.query.all()
    return render_template("qna.html", email=email, show_users=show_users)

@app.route("/creator")
def creator():
    return render_template("creator.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
