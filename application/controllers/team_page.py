#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application.models.player_manager import *
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.file_manager import *
import json
import logging
@app.route('/teampage/<int:team_pk>', methods=['GET'])
def teampage(team_pk):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	team_instance = Team.query.get(team_pk)

	team_match_list = get_match_list_by_team(team_pk)
	match_pk_list = []
	for item in team_match_list:
		new_pk = item.match_pk
		match_pk_list.append(new_pk)

	match_list = []
	for i in match_pk_list:
		score = get_match_result_by_match_pk(i)
		match = get_match_by_match_pk(i)
		match_dic = {}
		match_dic['year'] = match.date.year
		match_dic['month'] = match.date.month
		match_dic['day'] = match.date.day
		match_dic['hour'] = match.date.hour

		if str(match.date.minute) == "0":
			match_dic['minute'] = str(match.date.minute)+'0'
		else:
			match_dic['minute'] = match.date.minute
	
		round = find_round(match.round_pk)
		match_dic['round'] = round
		score.append(match_dic)
		match_list.append(score)

	lank_instance = get_point_list_by_desc(2)
	lank_list = []
	for item in lank_instance:
		lank_list.append(item.pk)
	#팀등록만되었을떄 lanking부분 에러
	lanking = lank_list.index(team_pk) + 1

	player_instance = get_players_by_team_pk(team_pk)

	goal_rank=get_player_rank_in_team(team_pk, 1)
	assist_rank=get_player_rank_in_team(team_pk, 2)
	match_rank=get_player_rank_in_team(team_pk, 3)
	yellow_rank=get_player_rank_in_team(team_pk, 4)
	red_rank=get_player_rank_in_team(team_pk, 5)
	limit_rank=get_player_rank_in_team(team_pk, 6)

	if get_best_11_player(team_pk)!=[]:
		best_11=get_best_11_player(team_pk)
		best_11_message=""
	else:
		best_11={}
		best_11_message=u"아직 best11이 등록되지 않았습니다."
	return render_template('teampage.html',best_11_message=best_11_message,best_11=best_11,team_instance=team_instance, match_list=match_list, lanking=lanking, player_instance=player_instance,goal_rank=goal_rank,assist_rank=assist_rank,yellow_rank=yellow_rank,red_rank=red_rank,match_rank=match_rank,limit_rank=limit_rank)

@app.route('/player_popup', methods=['GET','POST'])
def player_popup():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	if request.method == 'POST':
		# raise ValueError(request.form['id'])
		pk=request.form['player_pk']
		pk=int(pk)
		player=Player.query.get(pk)
		return render_template('player_hover.html',player=player)
	else:
		return render_template('player_hover.html')

@app.route('/get_profile_image/<filename>')
def get_profile_image(filename):
	if 'logged_in' not in session:
		return redirect(url_for('index'))
		
	new_filename=filename.split('.')[0]
	directory = '/gs/kchamps/img/Users/'+str(new_filename)+'/profile/'
	filepath = directory + filename.encode('utf8')
	return read_file(filepath)

@app.route('/sort_players', methods=['GET','POST'])
def sort_players():
	if request.method=='POST':
		if request.form['data']=="1":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.player_name)).all()
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.player_name)).all()
		if request.form['data']=="2":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.college)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.college)).all()
		if request.form['data']=="3":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.major)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.major)).all()
		if request.form['data']=="4":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.position)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.position)).all()
		if request.form['data']=="5":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.student_id)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.student_id)).all()
		if request.form['data']=="6":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.goal)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.goal)).all()
		if request.form['data']=="7":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.assist)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.assist)).all()
		if request.form['data']=="8":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.match_count)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.match_count)).all()
		if request.form['data']=="9":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.yellow_card_count)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.yellow_card_count)).all()
		if request.form['data']=="10":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.red_card_count)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.red_card_count)).all()
		if request.form['data']=="11":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.limit_of_participation)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.limit_of_participation)).all()
		if request.form['data']=="12":
			if request.form['direction']=="1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.desc(Player.accumulate_limit_of_participation)).all()			
			if request.form['direction']=="-1":
				player_instance = Player.query.filter_by(team_pk=int(request.form['team_pk'])).order_by(db.asc(Player.accumulate_limit_of_participation)).all()


		list=[]
		for player in player_instance:
			dic={'player_name':""}
			dic['player_name']=player.player_name
			dic['student_id']=player.student_id
			dic['college']=player.college
			dic['major']=player.major
			dic['position']=player.position
			dic['goal']=player.goal
			dic['yellow_card_count']=player.yellow_card_count
			dic['red_card_count']=player.red_card_count
			dic['limit_of_participation']=player.limit_of_participation
			dic['match_count']=player.match_count
			dic['accumulate_limit_of_participation']=player.accumulate_limit_of_participation
			dic['assist']=player.assist
			list.append(dic)
		return json.dumps(list)