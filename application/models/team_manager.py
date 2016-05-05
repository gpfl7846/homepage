#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from sqlalchemy import or_
from application.models.player_manager import *
from application.models.match_manager import *
import datetime
from sqlalchemy import text, exc, insert
import logging

def get_team(id):
	return Team.query.get(id)

def compare_team_goal(match_pk):
	match_team=Match_team.query.filter_by(match_pk=match_pk).all()
	match_team1=match_team[0]
	match_team2=match_team[1]
	# logging.debug(match_team1.team_goal)
	# logging.debug(match_team2.team_goal)
	
	#team1이 이겼을 때
	if int(match_team1.team_goal)>int(match_team2.team_goal):
		win_team_pk=match_team1.team_pk
		input_win(match_team1.team_pk)
		input_lose(match_team2.team_pk)

		goals_forA = int(get_team(match_team1.team_pk).goals_for) + match_team1.team_goal
		goals_againstA = int(get_team(match_team1.team_pk).goals_against) + match_team2.team_goal
		goals_differenceA = goals_forA - goals_againstA
		input_goal_result(match_team1.team_pk,goals_forA,goals_againstA,goals_differenceA)

		goals_forB = int(get_team(match_team2.team_pk).goals_for) + match_team2.team_goal
		goals_againstB = int(get_team(match_team2.team_pk).goals_against) + match_team1.team_goal
		goals_differenceB = goals_forB - goals_againstB
		input_goal_result(match_team2.team_pk,goals_forB,goals_againstB,goals_differenceB)

	#team2가 이겼을 떄
	elif int(match_team1.team_goal)<int(match_team2.team_goal):
		win_team_pk=match_team2.team_pk
		input_win(match_team2.team_pk)
		input_lose(match_team1.team_pk)

		goals_forA = int(get_team(match_team1.team_pk).goals_for) + match_team1.team_goal
		goals_againstA = int(get_team(match_team1.team_pk).goals_against) + match_team2.team_goal
		goals_differenceA = goals_forA - goals_againstA
		input_goal_result(match_team1.team_pk,goals_forA,goals_againstA,goals_differenceA)

		goals_forB = int(get_team(match_team2.team_pk).goals_for) + match_team2.team_goal
		goals_againstB = int(get_team(match_team2.team_pk).goals_against) + match_team1.team_goal
		goals_differenceB = goals_forB - goals_againstB
		input_goal_result(match_team2.team_pk,goals_forB,goals_againstB,goals_differenceB)

	#둘다 비겼을 때
	elif int(match_team1.team_goal)==int(match_team2.team_goal):
		win_team_pk=1
		input_draw(match_team1.team_pk)
		input_draw(match_team2.team_pk)
		
		goals_forA = int(get_team(match_team1.team_pk).goals_for) + match_team1.team_goal
		goals_againstA = int(get_team(match_team1.team_pk).goals_against) + match_team2.team_goal
		
		goals_forB = int(get_team(match_team2.team_pk).goals_for) + match_team2.team_goal
		goals_againstB = int(get_team(match_team2.team_pk).goals_against) + match_team1.team_goal

		input_draw_goal_result(match_team1.team_pk,goals_forA,goals_againstA)
		input_draw_goal_result(match_team2.team_pk,goals_forB,goals_againstB)	

	# logging.debug(win_team_pk)
	match=Match.query.get(match_pk)
	match.win_team_pk=win_team_pk
	db.session.commit()

def input_win(team_pk):
	team=Team.query.get(team_pk)
	team.win+=1
	team.team_match_count+=1
	team.point+=3
	db.session.commit()

def input_lose(team_pk):
	team=Team.query.get(team_pk)
	team.lose+=1
	team.team_match_count+=1
	db.session.commit()

def input_draw(team_pk):
	team=Team.query.get(team_pk)
	team.draw+=1
	team.team_match_count+=1
	team.point+=1
	db.session.commit()

def input_draw_goal_result(team_pk,goals_against,goals_for):
	team=Team.query.get(team_pk)
	team.goals_against=goals_against
	team.goals_for=goals_for
	db.session.commit()

def input_goal_result(team_pk,goals_against,goals_for,goal_difference):
	team=Team.query.get(team_pk)
	team.goals_against=goals_against
	team.goals_for=goals_for
	team.goal_difference=goal_difference
	db.session.commit()	

def get_rank_team_list(league):
	team_rank_list=[]
	cnt=1
	for team in Team.query.filter_by(league=league).order_by(db.desc(Team.point),db.desc(Team.goal_difference),db.desc(Team.goals_for),db.asc(Team.goals_against)).slice(0,20):
		#User.query.order_by(User.popularity.desc(),User.date_created.desc()).limit(10).all()
		rank_dic={}
		t=Team.query.get(team.pk)
		rank_dic['rank']=cnt
		rank_dic['name']=t.name
		rank_dic['win']=t.win
		rank_dic['draw']=t.draw
		rank_dic['lose']=t.lose
		rank_dic['point']=t.point
		rank_dic['goals_for']=t.goals_for
		rank_dic['goal_difference']=t.goal_difference
		rank_dic['goals_against']=t.goals_against
		team_rank_list.append(rank_dic)
		cnt+=1
	return team_rank_list

def add_team(data):
	team=Team(
		name=data['teamname'],
		college=data['college']
		)
	db.session.add(team)
	db.session.commit()
	return team.pk

def add_team_img(team_pk, filename):
	team= get_team(team_pk)
	team.team_img =filename
	db.session.commit()

def delete_team(team_pk):
	d_team=Team.query.get(team_pk)
	db.session.delete(d_team)
	db.session.commit()


def get_players_by_team_pk(t_pk):
	list=Player.query.filter_by(team_pk=t_pk).all()
	# player_pk_list=[]
	# player_name_list=[]
	# for i in list:
	# 	player_pk_list.append(i.pk)

	# for j in player_pk_list:
	# 	player_name_list.append(Player.query.get(j))
	return list	

def get_best_11_player(team_pk):
	match_pk=Match.query.filter(Match.win_team_pk!=None).order_by(db.desc(Match.date)).with_entities(Match.pk).first()
	best_11=[]
	if match_pk[0]!=None:
		match_team_pk=Match_team.query.filter(Match_team.match_pk==match_pk[0],Match_team.team_pk==team_pk).with_entities(Match_team.pk).first()
		if match_team_pk:
			player_pk_list=Match_player.query.filter(Match_player.match_team_pk==match_team_pk[0]).with_entities(Match_player.player_pk).all()	
			for player_pk in player_pk_list:
				best_11.append(Player.query.filter(Player.pk==player_pk[0]).with_entities(Player.pk,Player.player_name,Player.position,Player.wildcard).all())
			return best_11
		else:
			return best_11
	else:
		return best_11

def get_match_count(team_pk):
	return Team.query.filter_by(pk=team_pk).with_entities(Team.team_match_count).first()[0]