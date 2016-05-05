#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application import db
from sqlalchemy import or_,and_
from application.models.match_manager import *
from application.models.notification_manager import *
from application.models.password_manager import *
from notification import confirm_match_result_notification, match_notification_before_2day,request_match_result_notification
import logging
from datetime import timedelta, datetime, tzinfo
from pytz import timezone
import pytz

utc=pytz.utc
korea=timezone('Asia/Seoul')

@app.route('/match_notification_trigger/<int:match_pk>')
def match_notification_trigger(match_pk):
	match_date=Match.query.filter_by(pk=match_pk).with_entities(Match.date).first()
	date_time = match_date[0] + timedelta(days=-1)
	t_time=int(time.mktime(date_time.timetuple()))

	return render_template('message.html', t_time=t_time)

@app.route('/find_match_tomorrow')
def find_match_tomorrow():
	matches=Match.query.filter(Match.pk!=None).with_entities(Match.date, Match.pk).all()
	# logging.debug(korea.localize(datetime.now()))
	for match_date in matches:
		# logging.debug(match_date[0])
		if timedelta(days=1)<(korea.localize(match_date[0]) - datetime.now(korea))< timedelta(days=3) :
			# logging.debug(match_date[1])
			# logging.debug('yes')
			#알림생성
			n_pk=Notification.query.filter(and_(Notification.match_pk==match_date[1], Notification.type_pk==9)).with_entities(Notification.pk).all()
			if n_pk != None:
				for i in n_pk:
					delete_notification(i[0])

			match_notification_before_2day(match_date[1])

		# else:
		# 	logging.debug(match_date[1])
		# 	logging.debug('no')

	# date_time = match_date[0] + timedelta(days=-1)
	return redirect(url_for('index'))

@app.route('/request_match_result')
def request_match_result():
	matches=Match.query.filter(Match.pk!=None).with_entities(Match.date, Match.pk, Match.referee_pk).all()
	# logging.debug(korea.localize(datetime.now()))
	for match_date in matches:
		# logging.debug(match_date[0])
		if timedelta(days=0)<( datetime.now(korea)-korea.localize(match_date[0]))< timedelta(days=1) :
			# logging.debug(match_date[1])
			# logging.debug('yes')
			# logging.debug(match_date[2])
			#알림생성
			request_match_result_notification(match_date[1], match_date[2])
		# else:
		# 	logging.debug(match_date[1])
		# 	# logging.debug('no')

	return redirect(url_for('index'))

@app.route('/find_overtime_key')
def find_overtime_key():
	rows=Password_change.query.filter(Password_change.pk!=None).all()
	for row in rows:
		if timedelta(days=1)<( datetime.now(korea)-korea.localize(row.time)) :
			db.session.delete(row)
			db.session.commit()
	return redirect(url_for('index'))