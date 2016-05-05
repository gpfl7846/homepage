#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.file_manager import *
from application.models.player_manager import *
from notification import confirm_match_result_notification,limitation_notification,free_limitation_notification
import logging
import json

@app.route('/get_teamlogo_after_match/<filename>')
def get_teamlogo_after_match(filename):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	new_filename=filename.split('.')[0]
	directory='/gs/kchamps/img/Team/'+str(new_filename)+'/logo/'
	filepath = directory + filename.encode('utf8')
	return read_file(filepath)

@app.route('/after_match/<int:match_pk>', methods=['GET'])
def after_match(match_pk):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	m_instance = get_match_by_match_pk(match_pk)
	match_dic = {}
	match_dic['pk'] = match_pk
	match_dic['year'] = m_instance.date.year
	match_dic['month'] = m_instance.date.month
	match_dic['day'] = m_instance.date.day
	match_dic['hour'] = m_instance.date.hour
	if m_instance.date.minute == 0: 
		match_dic['minute'] = str(m_instance.date.minute) + '0'
	else:
		match_dic['minute']	= m_instance.date.minute
	match_dic['location'] = m_instance.location

	match_result = get_match_result_by_match_pk(match_pk)
	team_pk_list = get_team_list_by_match_pk(match_pk)
	team_list = []
	player_list = []
	goal_list = []
	for item in match_result:
		goal = item['goal']
		goal_list.append(goal)

	for i in team_pk_list:
		team_info = {}
		team_inst = get_team(i)
		team_info['pk'] = i
		team_info['name'] = team_inst.name
		team_info['college'] = team_inst.college
		team_info['img'] = team_inst.team_img
		team_list.append(team_info)

		p_list = get_match_player_list(match_pk, i)		
		best11_list = []
		for item in p_list:
			player_pk = item.player_pk
			player_inst = get_player(player_pk)
			best11_list.append(player_inst)
		player_list.append(best11_list)
	status_list=get_status_list()
	match=Match.query.get(match_pk)
	if goal_list == []:
		return render_template('after_match.html', match_dic=match_dic, team_list=team_list, player_list=player_list, status_list=status_list,match=match)
	
	else:
		return render_template('after_match.html', match_dic=match_dic, team_list=team_list, player_list=player_list, goal_list=goal_list, status_list=status_list,match=match)

@app.route('/input_match_result',methods=['POST'])
def input_match_result():
	if request.method=="POST":
		match_pk=request.form['matchpk']
		team_pk=request.form['selectTeam']
		player_pk=request.form['selectPlayer']
		time=request.form['selectTime']
		status_pk=request.form['selectStatus']
		input_result_for_timeline(match_pk,team_pk,player_pk,time,status_pk) #match_result테이블에 입력
		if int(status_pk)==2: #득점이면
			input_team_goal(match_pk,team_pk) #match_team테이블에 team_goal입력

		return redirect(url_for('after_match', match_pk=match_pk))

#경기결과 입력이 완료된 경우에만 한 번 돌릴 것
@app.route('/update_team_table/<int:match_pk>')
def update_team_table(match_pk):
	compare_team_goal(match_pk) #team테이블에 골득실, 승무패 계산
	# confirm_match_result_notification(matchpk) #경기결과가 등록되었다는 알림 생성
	find_red_and_yellow_card(match_pk)
	match_team=Match_team.query.filter_by(match_pk=match_pk).all()
	match_team1=match_team[0]
	match_team2=match_team[1]
	set_player_match_count_tmp(match_team1.team_pk)
	set_player_match_count_tmp(match_team2.team_pk)
	compare_team_match_count(match_team1.team_pk)
	compare_team_match_count(match_team2.team_pk)
	return redirect(url_for('after_match',match_pk=match_pk))

@app.route('/set_player_match_count_tmp/<int:team_pk>')
def set_player_match_count_tmp(team_pk):
	count=get_match_count(team_pk)
	players=Player.query.filter(and_(Player.team_pk==team_pk, Player.limit_of_participation>0)).with_entities(Player.pk).all()
	for pk in players:
		logging.debug(pk[0])
		player=Player.query.get(pk[0])
		player.match_count_tmp=count
		db.session.commit()
	return None

#출전제한 감소시킴
@app.route('/compare_team_match_count/<int:team_pk>')
def compare_team_match_count(team_pk):
	count=int(get_match_count(team_pk))
	players=Player.query.filter(and_(Player.team_pk==team_pk, Player.limit_of_participation>0)).with_entities(Player.pk).all()
	logging.debug(count)
	for pk in players:
		logging.debug(pk[0])
		player=Player.query.get(pk[0])
		if player.match_count_tmp!=count:
			logging.debug('1')
			player.match_count_tmp=player.match_count_tmp+1
			player.limit_of_participation=player.limit_of_participation-1
			db.session.commit()

			if Player.query.filter_by(pk=player.pk).with_entities(Player.limit_of_participation).first()[0] ==0:
				player.match_count_tmp = 0
				db.session.commit()
				free_limitation_notification(pk[0])

	return None	

#그 경기에서 최소한 경고이상 받았던 사람들 분류해서 입력
@app.route('/find_red_and_yellow_card/<int:m_pk>')
def find_red_and_yellow_card(m_pk):
	pk_list=[]
	results=Match_result.query.filter(and_(Match_result.match_pk==m_pk, or_(Match_result.status_pk==5, Match_result.status_pk==6))).with_entities(Match_result.player_pk).all()
	for pk in results:
		if pk[0] not in pk_list:
			pk_list.append(pk[0])
	# logging.debug(pk_list)
	for player_pk in pk_list:
		result_for_red_and_yellow_card(m_pk, player_pk)
	return None

@app.route('/result_for_red_and_yellow_card/<int:match_pk>/<int:player_pk>')
def result_for_red_and_yellow_card(match_pk, player_pk):
	red=int(count_red_card_in_match_result(match_pk, player_pk))
	yellow=int(count_yellow_card_in_match_result(match_pk, player_pk))
	logging.debug(player_pk)
	logging.debug(yellow)
	logging.debug(red)
	player= Player.query.get(player_pk)
	if yellow==2: #옐로우 카드 두번받아서 퇴장한 경우
		if red==1: 
			player.red_card_count=player.red_card_count+1
			player.limit_of_participation=player.limit_of_participation+1
			player.accumulate_limit_of_participation=player.accumulate_limit_of_participation+1
			limitation_notification(player_pk)
			db.session.commit()
	if yellow<2:
		if red==1:	#엘로우 카드 1번 받았는데 즉시 퇴장 명령받으면			
			player.yellow_card_count=player.yellow_card_count+yellow
			player.red_card_count=player.red_card_count+1
			player.limit_count=player.limit_count+yellow
			player.limit_of_participation=player.limit_of_participation+2
			player.accumulate_limit_of_participation=player.accumulate_limit_of_participation+2
			limitation_notification(player_pk)
			db.session.commit()
		else: #옐로 카드만 받았을 경우
			player.yellow_card_count=player.yellow_card_count+yellow
			player.limit_count=player.limit_count+yellow
			db.session.commit()

	if_limit_count_3(player_pk)
	return None

@app.route('/search_goaler', methods=['POST'])
def search_goaler():
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