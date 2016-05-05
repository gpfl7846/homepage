#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from application.models.schema import *
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.player_manager import *
from application.models.file_manager import *
from notification import lineup_notification,lineup_notification_for_captains
import json
import logging

@app.route('/get_teamlogo_image_before_match/<filename>')
def get_teamlogo_image_before_match(filename):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	new_filename=filename.split('.')[0]
	directory='/gs/kchamps/img/Team/'+str(new_filename)+'/logo/'
	filepath = directory + filename.encode('utf8')

	return read_file(filepath)	

@app.route('/before_match/<int:match_pk>', methods=['GET'])
def before_match(match_pk):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	match_instance = get_match_by_match_pk(match_pk)
	match_dic = {}
	match_dic['year'] = match_instance.date.year
	match_dic['month'] = match_instance.date.month
	match_dic['day'] = match_instance.date.day
	match_dic['hour'] = match_instance.date.hour
	if str(match_instance.date.minute) == "0":
		match_dic['minute'] = str(match_instance.date.minute)+'0'
	else:
		match_dic['minute'] = match_instance.date.minute
	match_dic['location'] = match_instance.location
	match_dic['pk'] = match_pk

	team_pk_list = get_team_list_by_match_pk(match_pk)
	team_list = []
	player_list = []
	for i in team_pk_list:
		team_info = {}
		team_instance = get_team(i)
		team_name = team_instance.name
		team_img = team_instance.team_img
		team_info['pk'] = i
		team_info['name'] = team_name
		team_info['img'] = team_img
		team_list.append(team_info)
		p_list = get_match_player_list(match_pk, i)
		best11_list = []
		for item in p_list:
			player_pk = item.player_pk
			player_instance = get_player(player_pk)
			best11_list.append(player_instance)
		player_list.append(best11_list)
	return render_template('before_match.html', match_dic=match_dic, team_list=team_list, player_list=player_list)

@app.route('/show_lineup', methods=['POST'])
def show_lineup():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	team_pk = request.form['team_pk']
	player_instance = get_players_by_team_pk(team_pk)
	send_list = []
	for item in player_instance:
		#출전제한 없는 선수들만 라인업 등록할 수 있음
		if item.limit_of_participation==0:
			player_dic={}
			player_dic['pk'] = item.pk
			player_dic['name'] = item.player_name
			player_dic['major'] = item.major
			player_dic['position'] = item.position
			player_dic['student_id'] = item.student_id
			send_list.append(player_dic)

	return json.dumps(send_list)

@app.route('/register_lineup', methods=['POST'])
def register_lineup():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	player_id = int(request.form['player_id'])
	
	team_pk = get_player(player_id).team_pk
	match_pk = int(request.form['match_pk'])
	player_list = get_match_player_list(match_pk, team_pk)

	if len(player_list) < 11:
		player_check = []
		for i in player_list:
			p_pk = int(i.player_pk)
			player_check.append(p_pk)

		# logging.debug(player_id)
		# logging.debug(player_check)
		# logging.debug(player_id in player_check)

		if player_id not in player_check:
			# logging.debug('here')
			p_instance = get_player(player_id)
			add_match_player(match_pk, player_id)
			lineup_notification(match_pk, player_id, session['user_pk'])

			player_check.append(player_id)
			send_list = []
			send_dic = {}
			send_dic['name'] = p_instance.player_name
			send_dic['pk'] = p_instance.team_pk
			send_dic['position'] = p_instance.position
			send_dic['player_id'] = player_id
			send_list.append(send_dic)
			return json.dumps(send_list)

		else:
			# logging.debug('there')
			return 'Already'

	elif len(player_list) >= 11:
		lineup_notification_for_captains(match_pk, session['user_pk'])
		return 'None'

@app.route('/search_player', methods=['POST'])
def search_player():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	name = request.form['result']
	pk_list = search_player_pk_by_player_name(name)
	send_list = []
	for i in pk_list:
		send_data = {}
		player_inst = get_player(i)
		send_data['pk'] = i
		send_data['name'] = player_inst.player_name
		send_data['major'] = player_inst.major
		send_data['student_id'] = player_inst.student_id
		send_list.append(send_data)
	return json.dumps(send_list)

@app.route('/add_referee', methods=['POST'])
def add_referee():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	date = request.form['match_date']
	hour = request.form['matchhour']
	minute = request.form['matchminute']
	return None