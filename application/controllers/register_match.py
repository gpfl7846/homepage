#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application.models.team_manager import *
from application.models.file_manager import *
from application.models.match_manager import *
from notification import register_match_notification
import datetime
from threading import *
import logging

@app.route('/addmatch')
def addmatch():
	if 'logged_in' not in session:
		return redirect(url_for('index'))
	league2list = get_team_list_by_league(2)
	return render_template('register_match.html', league2list=league2list)

@app.route('/registermatch', methods=['POST'])
def registermatch():
	if 'logged_in' not in session:
		return redirect(url_for('index'))
		
	round = request.form['matchround']
	date = datetime.datetime.strptime(request.form['matchdate'], "%Y-%m-%d")
	year = date.year
	month = date.month
	day = date.day
	hour = int(request.form['matchhour'])
	minute = int(request.form['matchminute'])

	matchdate = datetime.datetime.combine(datetime.date(year, month, day), datetime.time(hour, minute))
	location = request.form['matchlocation']
	
	match_pk = add_match(matchdate, location, round)
	add_match_team(match_pk, request.form['matchteam1'], request.form['matchteam2'])
	register_match_notification(session['user_pk'],match_pk, request.form['matchteam1'], request.form['matchteam2'])
	# match_notification_trigger(match_pk)
	return redirect(url_for('addmatch'))
