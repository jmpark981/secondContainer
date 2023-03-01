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
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://xxxxx:xxxxxxx@localhost/users"

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
    how_eat=db.Column(db.String(45), nullable=False)

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
    how_eat=MultiCheckBoxField("5. 식사해결방법", choices=[('기숙사 식당', '기숙사 식당'), ('외식', '외식'), ('기숙사 내', '기숙사 내')])
    submit=SubmitField("Submit")

    
@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/servey", methods=["GET", "POST"])
def servey():
    email=None
    age=0
    sex=None
    college_of=None
    how_eat=None
    error_msg=""
    form=UserForm(request.form)
    
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
            return render_template("servey.html", error_msg=error_msg, email=email, age=age, sex=sex, college_of=college_of, how_eat=how_eat, form=form)
        else:
            user=Usertbl(email=form.email.data, age=form.age.data, sex=form.sex.data, college_of=form.college_of.data, how_eat="&".join(form.how_eat.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('qna', email=form.email.data))
        
        #Clear Form
        form=UserForm(formdata=None)
    
    return render_template("servey.html", error_msg=error_msg, email=email, age=age, sex=sex, college_of=college_of, how_eat=how_eat, form=form)

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
