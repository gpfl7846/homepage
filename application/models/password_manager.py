#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from sqlalchemy import or_, and_,sql
from application.models.team_manager import *
from application.models.match_manager import *
from application.controllers.notification import limitation_notification
import logging
from datetime import timedelta, datetime, tzinfo
from pytz import timezone
import pytz

utc=pytz.utc
korea=timezone('Asia/Seoul')

def create_password_change(user_email, key_string):
	password_change = Password_change(
		email 		= 	user_email,
		time 		= datetime.now(korea),	
		key 		= db.func.md5(key_string)
	)	
	db.session.add(password_change)
	db.session.commit()

#만약에 비밀번호 찾을 때 그이전에 요청한 것이 있으면 삭제
def is_exist_password_change_row(email):
	if Password_change.query.filter_by(email=email).count()!=0:
		row=Password_change.query.filter_by(email=email).first()
		db.session.delete(row)
		db.session.commit()
