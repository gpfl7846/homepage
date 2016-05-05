#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application.models.team_manager import *
from application.models.file_manager import *

@app.route('/addteam')
def addteam():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	return render_template('register_team.html')
	
@app.route('/registerteam', methods=['POST'])
def registerteam():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	team_pk=add_team(request.form)
	image_file = request.files['teamlogo']
	filename = image_file.filename
	extension = filename.split('.')[-1]
	new_file_name = str(team_pk) + '.' + extension.encode('utf8')
	directory = '/gs/kchamps/img/Team/'+str(team_pk)+'/logo/'
	filepath = directory + new_file_name
	save_file(image_file, filepath)
	return redirect(url_for('index'))