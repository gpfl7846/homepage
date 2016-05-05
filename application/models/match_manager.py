#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from application.models.player_manager import *
from application.models.team_manager import *
import datetime
from sqlalchemy import or_, and_
from sqlalchemy import text, exc, insert
import logging

def input_team_goal(match_pk, team_pk):
	match_team=Match_team.query.filter(and_(Match_team.match_pk==match_pk,Match_team.team_pk==team_pk)).first()
	match_team.team_goal=match_team.team_goal+1
	db.session.commit()
	# return match_team.pk

def input_result_for_timeline(match_pk,team_pk,player_pk,time,status):
	match = Match_result(
		match_pk=match_pk,
		team_pk=team_pk,
		player_pk=player_pk,
		time=time,
		status_pk=status
	)
	db.session.add(match)
	db.session.commit()
	return match.pk

def count_yellow_card_in_match_result(m_pk, p_pk):
	results=Match_result.query.filter(and_(Match_result.match_pk==m_pk, Match_result.player_pk==p_pk, Match_result.status_pk==5)).all()
	return len(results)

def count_red_card_in_match_result(m_pk, p_pk):
	results=Match_result.query.filter(and_(Match_result.match_pk==m_pk, Match_result.player_pk==p_pk, Match_result.status_pk==6)).all()
	return len(results)

def get_yellow_and_red_card(m_pk):
	list=[]
	players=Match_player.query.with_entities(Match_player.player_pk, Match_player.red_card, Match_player.yellow_card).filter(and_(Match_player.match_pk==m_pk,or_(Match_player.yellow_card!=None,Match_player.red_card!=None))).all()
	for player in players:
		p_dic={}
		p_dic['name']=Player.query.get(player.player_pk).player_name
		# p_dic['name']=get_player(player.player_pk).player_name
		p_dic['yellow_card']=player.yellow_card
		p_dic['red_card']=player.red_card
		list.append(p_dic)
	return list

def update_match_referee(match_pk, rt_pk, r_pk, ar1_pk, ar2_pk, fo_pk):
	match=Match.query.get(match_pk)
	match.referee_team_pk=rt_pk
	match.referee_pk=r_pk
	match.assistant_referee_1_pk=ar1_pk
	match.assistant_referee_2_pk=ar2_pk
	match.fourth_official_pk=fo_pk
	db.session.commit()

def update_match_info(match_pk, location, date, r_pk, ar1_pk, ar2_pk, fo_pk):
	#match정보를 수정
	match=Match.query.get(match_pk)
	match.location=location
	match.date=date
	match.referee_pk=r_pk
	match.assistant_referee_1_pk=ar1_pk
	match.assistant_referee_2_pk=ar2_pk
	match.fourth_official_pk=fo_pk
	db.session.commit()

def input_win_team_pk(m_pk, team_pk):
	match=Match.query.get(m_pk)
	match.win_team_pk=team_pk
	db.session.commit()

def get_referee_info_by_match_pk(m_pk):
	r_dic={}
	match=get_match_by_match_pk(m_pk)
	r_dic['referee_team']=Team.query.get(match.referee_team_pk).name
	r_dic['referee']=Player.query.get(match.referee_pk).player_name
	r_dic['assistant_referee_1']=Player.query.get(match.assistant_referee_1_pk).player_name
	r_dic['assistant_referee_2']=Player.query.get(match.assistant_referee_2_pk).player_name
	r_dic['fourth_official']=Player.query.get(match.fourth_official_pk).player_name
	return r_dic

def get_permutation_player_list_by_match_pk(m_pk):
	list=[]
	players=Match_player.query.filter(and_(Match_player.match_pk==m_pk,or_(Match_player.status_pk==2,Match_player.status_pk==3))).all()
	for player in players:
		p_dic={}
		p_dic['name']=Player.query.get(player.player_pk).player_name
		p_dic['status']=Status.query.get(player.status_pk).status
		# p_dic['name']=get_player(player.player_pk).player_name
		# p_dic['status']=get_status(player.status_pk)
		list.append(p_dic)
	return list

def get_round_by_season_and_league(round, season, league):
	return Round.query.filter(and_(Round.season==season,Round.league==league, Round.round==round)).first()

def get_match_list_by_team(team_pk):
	match_list=Match_team.query.filter_by(team_pk=team_pk).all()	
	return match_list

def get_match_by_match_pk(match_pk):
	return Match.query.get(match_pk)

def get_match_list_by_round(round_value,season,league):
	list=[]
	round_id=Round.query.filter(and_(Round.round==round_value,Round.season==season, Round.league==league)).with_entities(Round.pk).first()
	for i in Match.query.filter_by(round_pk=round_id[0]).with_entities(Match.pk).all():
		list.append(i[0])
	return list

def get_point_list_by_desc(league):
	return Team.query.filter_by(league=league).order_by(db.desc(Team.point)).all()

def get_next_match():
	next_match=Match.query.filter(Match.win_team_pk!=None).order_by(db.desc(Match.date)).with_entities(Match.round_pk).first()
	round= Round.query.filter_by(pk=next_match[0]).with_entities(Round.round).first()
	return round[0]

def season_next_match():
	next_match=Match.query.order_by(db.desc(Match.date)).first()
	return find_round(next_match.round_pk)

def get_team_list_by_league(league):
	return Team.query.filter_by(league=league).all()

def get_goal_point_by_match_and_team(match_pk,team_pk):
	goal= Match_team.query.filter(and_(Match_team.match_pk ==match_pk,Match_team.team_pk==team_pk )).with_entities(Match_team.team_goal)
	return goal[0]

def get_match_result_by_match_pk(match_pk):
	teams= Match_team.query.filter_by(match_pk=match_pk).with_entities(Match_team.team_pk).all()
	list=[]
	for team in teams:
		team_pk = team[0]
		team_info={}
		team_info['match_pk']=match_pk
		team_info['name']=Team.query.filter_by(pk=team_pk).with_entities(Team.name).first()[0] #각각 경기한 팀이름
		team_info['goal']=get_goal_point_by_match_and_team(match_pk,team_pk)[0] #match 각팀의 goal득점수 
		list.append(team_info)
	return list

def get_team_list_by_match_pk(match_pk):
	teams=Match_team.query.filter_by(match_pk=match_pk).all()
	team_pk_list=[]
	for i in teams:
		team_pk_list.append(i.team_pk)
	return team_pk_list

def add_match(date_,location_,round_):
	match = Match(
		date = date_,
		location= location_,
		round_pk=set_round_pk(round_)
	)
	db.session.add(match)
	db.session.commit()
	return match.pk

def add_match_team(m_pk, team_pk1, team_pk2):
	match_team1 = Match_team(
		match_pk = m_pk,
		team_pk = team_pk1
		)
	match_team2 = Match_team(
		match_pk = m_pk,
		team_pk = team_pk2
		)
	db.session.add(match_team1)
	db.session.add(match_team2)
	db.session.commit()

def update_match(match_pk, team_pk, team_goal):
	match_team=Match_team.query.filter(and_(Match_team.match_pk==match_pk, Match_team.team_pk==team_pk)).first()
	match_team.team_goal=team_goal
	db.session.commit()

def find_round(round_pk):
	return Round.query.get(round_pk).round

def set_round_pk(round_value):
	return Round.query.filter_by(round=round_value).first().pk

def match_info(match_pk):
	info_list=[]
	match_info={}
	match_info['date']=get_match_by_match_pk(match_pk).date
	match_info['location']=get_match_by_match_pk(match_pk).location
	info_list.append(match_info)
	return info_list

def add_match_player(match_pk,player_pk):
	player_team_pk=Match_team.query.filter(and_(Match_team.match_pk==match_pk, Match_team.team_pk==Player.query.get(player_pk).team_pk)).first()
	match_player = Match_player(
		match_pk = match_pk,
		player_pk = player_pk,
		match_team_pk = player_team_pk.pk
		)
	db.session.add(match_player)
	db.session.commit()

def delete_match_player(match_pk, player_pk):
	player=Match_player.query.filter(and_(Match_player.match_pk==match_pk, Match_player.player_pk==player_pk)).first()
	db.session.delete(player)
	db.session.commit()
		
def delete_match(match_pk):
	match=Match.query.filter_by(pk=match_pk).first()
	db.session.delete(match)
	db.session.commit()

def get_match_player_list(match_pk, team_pk):
	match_team=Match_team.query.filter(and_(Match_team.match_pk==match_pk, Match_team.team_pk==team_pk)).first()
	return 	Match_player.query.filter(and_(Match_player.match_pk==match_pk, Match_player.match_team_pk==match_team.pk)).all()

def add_match_goal(match_pk_,player_pk_,time_):
	match_goal = Match_goal(
		match_pk = match_pk_,
		player_pk= player_pk_,
		goal_time=time_
	)
	db.session.add(match_goal)
	db.session.commit()

def update_match_referee_team(match_pk, rt_pk):
	#심판팀을 등록
	match=Match.query.get(match_pk)
	match.referee_team_pk=rt_pk
	db.session.commit()

#여기부터 수정한 함수
def update_referee(match_pk, r_pk):
	#match정보를 수정
	match=Match.query.get(match_pk)
	match.referee_pk=r_pk
	db.session.commit()

def update_assistant_referee1(match_pk, ar1_pk):
	#match정보를 수정
	match=Match.query.get(match_pk)
	match.assistant_referee_1_pk=ar1_pk
	db.session.commit()

def update_assistant_referee2(match_pk, ar2_pk):
	#match정보를 수정
	match=Match.query.get(match_pk)
	match.assistant_referee_2_pk=ar2_pk
	db.session.commit()

def update_fourth_official(match_pk, fo_pk):
	#match정보를 수정
	match=Match.query.get(match_pk)
	match.fourth_official_pk=fo_pk
	db.session.commit()
