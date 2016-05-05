#-*- coding:utf-8 -*-
from application import app
#
from application import db
#
from flask import render_template, redirect, url_for, session, request, flash
from application.models.schema import *
from application.models.player_manager import *
from datetime import datetime, timedelta
import logging

@app.route('/find',methods=['GET','POST'])
def find():
	if request.method=='POST':
		text=request.form['text']
		users=find_user(text)
		return render_template('user_list.html',users=users)
	else:
		return render_template('emulate.html')

@app.route('/emulate/<int:user_pk>')
def emulate(user_pk):
	if session['role']=="Admin":
		session['original_session_pk']=session['user_pk']
		new_user=Player.query.get(user_pk)
		session['email']=new_user.email
		session['username']=new_user.player_name
		session['user_pk']=new_user.pk
		session['role']=new_user.role
		session['team_pk']=new_user.team_pk
		session['logged_in'] = True
		# logging.debug('바뀌기전')
		# logging.debug(session['original_session_pk'])
		# logging.debug('바뀐후')
		# logging.debug(session['user_pk'])
		return redirect(url_for('find'))
	else:
		error=u"권한이 없습니다."
		# logging.debug(session['user_pk'])
		return render_template('emulate.html',error=error)		

@app.route('/back_to_original_session')
def back_to_original_session():
	original=Player.query.get(session['original_session_pk'])
	session['email']=original.email
	session['username']=original.player_name
	session['user_pk']=original.pk
	session['role']=original.role
	session['team_pk']=original.team_pk
	session['logged_in'] = True
	# logging.debug(session['user_pk'])
	return redirect(url_for('find'))