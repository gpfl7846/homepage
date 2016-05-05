#-*- coding:utf-8 -*-
from application import app
#
from application import db
#
from flask import render_template, redirect, url_for, session, request, flash
from application.models.schema import *
from application.models.player_manager import *
from application.models.file_manager import *
from application.models.notification_manager import *
from application.models.password_manager import *
import re
from datetime import datetime, timedelta
from flask.ext.wtf import Form
from wtforms import(
    StringField,
    PasswordField,
    SelectField
    )
from wtforms import validators
from notification import signup_notification
import logging
import time
import csv
#mailing
import webapp2
from google.appengine.api import mail

class Resetpasswordform(Form):
    password=PasswordField(
        u'password',
        [
            validators.data_required(message=u'please enter your password'),
            validators.Length(min=8, max=20, message=u'please enter 8~20 password')
        ],
        description={'placeholder':u'enteryour password'}
    )

    password_check=PasswordField(
        u'password_check',
        [
            validators.data_required(message=u'please enter your password_check'),
            validators.EqualTo('password', message=u'not same')     
        ],
        description={'placeholder':u'enteryour password_check'}
    )

class Loginform(Form):
    email=StringField(
        u'email',
        [
            validators.data_required(message=u'please enter your email'),
            validators.Email(message=u'use email form')
        ],
        description={'placeholder':u'kchamps@kchamps.com'}
        )
    password=PasswordField(
        u'password',
        [
            validators.data_required(message=u'please enter your password'),
        ],
        description={'placeholder':u'********'}
        )

class Signform(Form):
    username=StringField(
        u'username',
        [
            validators.data_required(message=u'please enter your name'),
        ],
        description={'placeholder':u'huhu'}
    )

    birthday=StringField(
        u'birthday',
        [
            validators.data_required(message=u'please enter your birthday'),
        ],
        description={'placeholder':u'ex-941205'}
    )

    university=SelectField(u'university', choices=[('3','snu')],coerce=unicode)

    college=StringField(
        u'college',
        [
            validators.data_required(message=u'please enter your college'),
        ],
        description={'placeholder':u'college of Engineering'}
    )

    major=StringField(
        u'major',
        [
            validators.data_required(message=u'What is your major?'),
        ],
        description={'placeholder':u'computer science'}
    )
    
    student_id=StringField(
        u'student_id',
        [
            validators.data_required(message=u'What is your student id?'),
        ],
        description={'placeholder':u'14'}
    )
    
    uniform_number=StringField(
        u'유니폼넘버',
        description={'placeholder':u'7'}
    )

    phone=StringField(
        u'mobile',
        [
            validators.data_required(message=u'please enter your mobile'),
        ],
        description={'placeholder':u'010-1111-1234'}
    )

    role=SelectField(u'role', choices=[('Player',u'선수'),('Captain',u'주장'),('Committee',u'운영위원회')],coerce=unicode)

    position=SelectField(u'position', choices=[('FW','FW'),('DF','DF'),('MF','MF'),('GK','GK'),('','none')],coerce=unicode)

    wildcard=SelectField(u'선수출신여부', choices=[('',u'해당없음'),('1',u'선수출신')],coerce=unicode)

    email=StringField(
        u'email',
        [
            validators.data_required(message=u'please enter your email'),
            validators.Email(message=u'use email form')
        ],
        description={'placeholder':u'kchamps@kchamps.com'}
    )

    password=PasswordField(
        u'password',
        [
            validators.data_required(message=u'please enter your password'),
            validators.Length(min=8, max=20, message=u'please enter 8~20 password')
        ],
        description={'placeholder':u'enteryour password'}
    )

    password_check=PasswordField(
        u'password_check',
        [
            validators.data_required(message=u'please enter your password_check'),
            validators.EqualTo('password', message=u'not same')     
        ],
        description={'placeholder':u'enteryour password_check'}
    )

class Editform(Form):
  
    birthday=StringField(
        u'birthday',
        [
            validators.data_required(message=u'please enter your birthday'),
        ],
        description={'placeholder':u'ex-941205'}
    )

    university=SelectField(u'university', choices=[('3','snu')],coerce=unicode)

    college=StringField(
        u'college',
        [
            validators.data_required(message=u'please enter your college'),
        ],
        description={'placeholder':u'college of Engineering'}
    )

    major=StringField(
        u'major',
        [
            validators.data_required(message=u'What is your major?'),
        ],
        description={'placeholder':u'computer science'}
    )

    uniform_number=StringField(
        u'유니폼넘버',
        description={'placeholder':u'7'},
        default=None
    )
    
    phone=StringField(
        u'mobile',
        [
            validators.data_required(message=u'please enter your mobile'),
        ],
        description={'placeholder':u'010-1111-1234'}
    )

    role=SelectField(u'role', choices=[('Player','player'),('Captain','captain'),('Committee','committee')],coerce=unicode)

    wildcard=SelectField(u'선수출신여부', choices=[('',u'해당없음'),('1',u'선수출신')],coerce=unicode)

    position=SelectField(u'position', choices=[('FW','FW'),('DF','DF'),('MF','MF'),('GK','GK'),('','none')],coerce=unicode)

    password=PasswordField(
        u'password',
        [
            validators.data_required(message=u'please enter your password'),
            validators.Length(min=8, max=20, message=u'please enter 8~20 password')
        ],
        description={'placeholder':u'enteryour password'}
    )

    password_check=PasswordField(
        u'password_check',
        [
            validators.data_required(message=u'please enter your password_check'),
            validators.EqualTo('password', message=u'not same')     
        ],
        description={'placeholder':u'enteryour password_check'}
    )
@app.route('/signup', methods = ['POST', 'GET'])
def signup():

    if 'logged_in' in session:
        return redirect(url_for('index'))

    if request.method=="POST":
        form=Signform()
        if form.validate_on_submit():

            if form.data['uniform_number']!="":
                pk=add_player_with_uniform_num(form.data)

            else:
                pk=add_player(form.data)

                if request.files['profile_img'].filename!="":
                    image_file = request.files['profile_img']
                    filename = image_file.filename
                    extension = filename.split('.')[-1]
                    new_file_name = str(pk) +'_'+str(str(time.mktime(datetime.now().timetuple())).split('.')[0])+'.' + extension.encode('utf8')
                    directory = '/gs/kchamps/img/Users/' + str(pk)+'/profile/'
                    filepath = directory + new_file_name
                    save_file(image_file, filepath)
                    add_profile_image(pk,new_file_name)
            signup_notification(request.form['selectTeam'],pk)
            player=Player.query.get(pk)
            player.auth_key=id_generator()
            db.session.commit()
            mail_to_user(pk)
            return redirect(url_for('login'))
        else:
            league2list = get_team_list_by_league(2)
            return render_template('signup.html',form=form,league2list=league2list)
    else:
        form=Signform()
        league2list = get_team_list_by_league(2)
        return render_template('signup.html',form=form,league2list=league2list)

@app.route('/login', methods = ['POST', 'GET'])
def login() :
    if 'logged_in' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        form=Loginform()
        if form.validate_on_submit():
            
            if login_check(form.email.data, form.password.data):
                user=Player.query.filter_by(email=form.email.data).with_entities(Player.email, Player.player_name, Player.pk, Player.role, Player.team_pk, Player.authorized).first()

                if user.authorized==1:
                    session['email']=user.email
                    session['username']=user.player_name
                    session['user_pk']=user.pk
                    session['role']=user.role
                    session['team_pk']=user.team_pk
                    session['logged_in'] = True
                
                    return redirect(url_for("index"))
                else:
                    login_error=u"이메일 인증이 필요합니다. 가입한 이메일에서 인증링크를 클릭해주세요"
                    return render_template('login.html',form=form,login_error=login_error)                    
            else:
                login_error="wrong email or password"
                return render_template('login.html',form=form,login_error=login_error)
        else:
            login_error="wrong email or password"
            return render_template('login.html',form=form,login_error=login_error)
    else:
        form=Loginform()
        return render_template('login.html',form=form)

@app.route('/edit_profile/<int:user_pk>',methods=['GET','POST'])
def edit_profile(user_pk):
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    if request.method=="POST":
        form=Editform()
        if form.validate_on_submit():
            if request.files['profile_img'].filename!="":
                edit_player(user_pk,form.data)
                image_file = request.files['profile_img']
                filename = image_file.filename
                extension = filename.split('.')[-1]
                new_file_name = str(user_pk)+'_'+str(str(time.mktime(datetime.now().timetuple())).split('.')[0])+ '.' + extension.encode('utf8')
                directory = '/gs/kchamps/img/Users/'+str(user_pk)+'/profile/'
                filepath = directory + new_file_name
                save_file(image_file, filepath)
                add_profile_image(user_pk,new_file_name)
                # return redirect(url_for('index'))
            else:
                edit_player(user_pk,form.data)
                # return redirect(url_for('index'))
            user_address = Player.query.get(user_pk).email
            confirmation_url = "kchamps.com"
            sender_address = "kchamps.com <dev.kchampsleague@gmail.com>"
            subject = "kchamps.com에서 정보수정이 되었습니다."
            body = """
        kchamps.com의 고객님의 개인정보가 수정되었습니다. 고객님 본인이 변경한 것이 아니면 고객센터로 연락하세요.
        %s
        """ % confirmation_url
            mail.send_mail(sender_address, user_address, subject, body)
            return redirect(url_for('index'))
        else:
            login_error=u"올바른 password를 입력하시오(8~20자)"
            user=get_player(user_pk)
            form=Editform(
                birthday=user.birthday,
                college=user.college,
                major=user.major,
                phone=user.phone,
                role=user.role,
                position=user.position,
                uniform_number=user.uniform_number,
                wildcard=user.wildcard
                )
        return render_template('edit_profile.html',profile_img=user.profile_img,user_pk=user_pk,form=form,user=user,login_error=login_error)
    else:
        user=get_player(user_pk)
        form=Editform(
            birthday=user.birthday,
            college=user.college,
            major=user.major,
            phone=user.phone,
            role=user.role,
            position=user.position,
            uniform_number=user.uniform_number,
            wildcard=user.wildcard
            )

        return render_template('edit_profile.html',profile_img=user.profile_img,user_pk=user_pk,form=form,user=user)

@app.route('/image/profile/<filename>')
def profile_img(filename):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
    if filename=="profile_default.png":
        directory = '/gs/kchamps/resource/'        
    else:
        directory = '/gs/kchamps/img/Users/'+str(session['user_pk'])+'/profile/'
    filepath = directory +filename
    return read_file(filepath)

@app.route('/logout')
def logout():
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    session.clear()
    return redirect(url_for("index"))

@app.route('/find_user',methods=['POST'])
def find_user():
    if request.method=='POST':
        input_email=str(request.form['text'])
        if Player.query.filter(Player.email==input_email).count()!=0:
            message="user exist"
            return message #user exist
        else:
            message="user not exist"
            return message #user not exist

@app.route('/check_password',methods=['POST'])
def check_password():
    if request.method=='POST':
        if bool(re.search("(?=.*\d)(?=.*[a-z])(?=.{8,20})",request.form['password']))==True:
            message_password="you can use password"
        else:
            message_password="you should change your password"
        return render_template('message.html',message_password=message_password)

@app.route('/check_password_check',methods=['POST'])        
def check_password_check():
    if request.method=='POST':
        if request.form['password_check']!=request.form['password']:
            message_password_check="different password"
        else:
            message_password_check="same!"
        return render_template('message.html',message_password_check=message_password_check)


@app.route('/group_signup', methods=['POST','GET'])
def group_signup():

    if request.method=='POST':

        lines=request.files['signuptool'].read().split("\n")[2:-1]
        for line in lines:
            item=line.split(',')

            player = Player(
                team_pk= request.form['selectTeam'],
                email    = item[1].decode('utf-8'),
                player_name = item[0].decode('utf-8'),
                major    = item[7].decode('utf-8'),
                student_id = item[3].decode('utf-8'),
                college = item[6].decode('utf-8'),
                password = db.func.md5(item[3].decode('utf-8')),
                phone    = item[4].decode('utf-8'),
                birthday = item[2].decode('utf-8'),
                role     = "Player",
                position    = item[5].decode('utf-8'),
            )   
            db.session.add(player)
            db.session.commit()

        return redirect(url_for('group_signup'))
    else:
        league2list = get_team_list_by_league(2)
        return render_template('group_signup.html', league2list=league2list)


@app.route('/mail_to_user/<int:pk>')
def mail_to_user(pk):

    user_address = Player.query.get(pk).email
    random_key=Player.query.get(pk).auth_key

    if not mail.is_email_valid(user_address):
        logging.debug('not valid email')

    else:
        # confirmation_url = createNewUserConfirmation(self.request)
        confirmation_url = "ryu.k-champsleague.appspot.com/authorized/"+str(random_key)
        sender_address = "kchamps.com <dev.kchampsleague@gmail.com>"
        subject = "회원가입 인증메일입니다."
        body = """
회원가입 후 이메일이 맞는지 확인하기 위한 메일입니다. 아래의 링크를 클릭해주세요.
Thank you for creating an account! Please confirm your email address by
clicking on the link below:

%s
""" % confirmation_url

        mail.send_mail(sender_address, user_address, subject, body)
    return None

@app.route('/authorized/<string:key>')
def authorized(key):
    player=Player.query.filter_by(auth_key=key).first()
    player.authorized=1
    #회원가입완료되었다는 메일 보낼것
    user_address = player.email
    confirmation_url = "kchamps.com"

    sender_address = "kchamps.com <dev.kchampsleague@gmail.com>"
    subject = "k챔스의 회원이 되신것을 축하드립니다."
    body = """
K-champs의 회원이 되신 것을 축하드립니다. 지금 바로 축구선수로서의 제2의 인생을 시작하세요.
%s
""" % confirmation_url
    mail.send_mail(sender_address, user_address, subject, body)
    db.session.commit()
    return redirect(url_for('login'))


@app.route('/find_password/', methods=['POST','GET'])
def find_password():
    if request.method=='POST':
        email=request.form['email']
        name=request.form['username']
       
        if Player.query.filter(Player.email==email,Player.player_name==name).count()!=0:
           
            player=Player.query.filter(Player.email==email,Player.player_name==name).first()
            user_address = player.email
            key_string=id_generator()
            is_exist_password_change_row(email)
            create_password_change(email, key_string)
            
            confirmation_url = "ryu.k-champsleague.appspot.com/reset_password/"+str(key_string)
            sender_address = "kchamps.com <dev.kchampsleague@gmail.com>"
            subject = "비밀번호 변경을 위한 메일입니다."
            body = """
            비밀번호가 초기화 되었습니다. 아래링크를 클릭하여 비밀번호를 재설정해 주십시오.
            Please confirm your email address by
            clicking on the link below:

            %s
            """ % confirmation_url

            mail.send_mail(sender_address, user_address, subject, body)
            error=u"메일이 발송되었으니 메일의 링크를 클릭하여 비밀번호 재설정을 해주세요."
            return render_template('find_password.html',error=error)
        else:
            logging.debug('not exist')
            error=u"일치하는 유저가 없습니다."
            return render_template('find_password.html', error=error)
    
    else:
        return render_template('find_password.html')

@app.route('/reset_password/<string:key>', methods=['POST','GET'])
def reset_password(key):
    key_string=db.func.md5(key)
    form=Resetpasswordform()
    if form.validate_on_submit():
        password_change_row=Password_change.query.filter_by(key=key_string).first()
        player=Player.query.filter_by(email=password_change_row.email).first()
        #비밀번호가 변경되었다는 메일
        user_address = player.email
        confirmation_url = "kchamps.com"
        sender_address = "kchamps.com <dev.kchampsleague@gmail.com>"
        subject = "kchamps.com의 비밀번호가 변경되었습니다."
        body = """
    kchamps.com의 고객님의 비밀번호가 변경되었습니다. 고객님 본인이 변경한 것이 아니면 고객센터로 연락하세요.
    %s
    """ % confirmation_url
        mail.send_mail(sender_address, user_address, subject, body)
        if str(form.data['password']) == str(form.data['password_check']) :
            player.password=db.func.md5(form.data['password'])
            db.session.delete(password_change_row)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('reset_password.html', n_key=key, form=form)
    else:
        if Password_change.query.filter_by(key=key_string).count()!=0:
            n_key=key
            return render_template('reset_password.html', n_key=n_key, form=form)