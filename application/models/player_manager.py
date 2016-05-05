#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from sqlalchemy import or_, and_,sql
from application.models.team_manager import *
from application.models.match_manager import *
from application.controllers.notification import limitation_notification
import datetime
import logging
import string
import random


def get_status_list():
	return Status.query.filter(Status.pk!=1).all()

def get_player_rank_in_team(team_pk,keyword):
	if keyword==1:
		goal=Player.query.filter(and_(Player.team_pk==team_pk, Player.goal!=0)).order_by(db.desc(Player.goal)).with_entities(Player.goal).first()
		if goal!=None:
			return Player.query.filter(Player.team_pk==team_pk, Player.goal==goal.goal).order_by(db.desc(Player.goal)).with_entities(Player.player_name,Player.goal).slice(0,2)
		else:
			return []
	if keyword==2:
		assist=Player.query.filter(and_(Player.team_pk==team_pk, Player.assist!=0)).order_by(db.desc(Player.assist)).with_entities(Player.assist).first()
		if assist!=None:
			return Player.query.filter(and_(Player.team_pk==team_pk, Player.assist==assist.assist)).order_by(db.desc(Player.assist)).with_entities(Player.player_name,Player.assist).slice(0,2)
		else:
			return []
	if keyword==3:
		match_count= Player.query.filter(and_(Player.team_pk==team_pk, Player.match_count!=0)).order_by(db.desc(Player.match_count)).with_entities(Player.match_count).first()
		if match_count!=None:
			return Player.query.filter(and_(Player.team_pk==team_pk, Player.match_count==match_count.match_count)).order_by(db.desc(Player.match_count)).with_entities(Player.player_name,Player.match_count).slice(0,2)
		else:
			return []
	if keyword==4:
		yellow=Player.query.filter(and_(Player.team_pk==team_pk, Player.yellow_card_count!=0)).order_by(db.desc(Player.yellow_card_count)).with_entities(Player.yellow_card_count).first()
		if yellow!=None:
			return Player.query.filter(and_(Player.team_pk==team_pk, Player.yellow_card_count==yellow.yellow_card_count)).order_by(db.desc(Player.yellow_card_count)).with_entities(Player.player_name,Player.yellow_card_count).slice(0,2)
		else:
			return []
	if keyword==5:
		red=Player.query.filter(and_(Player.team_pk==team_pk, Player.red_card_count!=0)).order_by(db.desc(Player.red_card_count)).with_entities(Player.red_card_count).first()
		if red!=None:
			return Player.query.filter(and_(Player.team_pk==team_pk, Player.red_card_count==red.red_card_count)).order_by(db.desc(Player.red_card_count)).with_entities(Player.player_name,Player.red_card_count).slice(0,2)
		else:
			return []
	if keyword==6:
		limit= Player.query.filter(and_(Player.team_pk==team_pk, Player.accumulate_limit_of_participation!=0)).order_by(db.desc(Player.accumulate_limit_of_participation)).with_entities(Player.accumulate_limit_of_participation).first()
		if limit!=None:
			return Player.query.filter(and_(Player.team_pk==team_pk, Player.accumulate_limit_of_participation==limit.accumulate_limit_of_participation)).order_by(db.desc(Player.accumulate_limit_of_participation)).with_entities(Player.player_name,Player.accumulate_limit_of_participation).slice(0,2)
		else:
			return []
def get_player_list_by_league(league): #리그속한 선수들 득점순 불러오기
	team_pk_list=[]
	rank_list=[]
	cnt=1
	# for team in get_team_list_by_league(league):
	for team in Team.query.filter_by(league=league).with_entities(Team.pk).all():
		team_pk_list.append(team[0])
	players=Player.query.filter(Player.team_pk.in_(team_pk_list)).order_by(db.desc(Player.goal)).with_entities(Player.player_name,Player.goal).slice(0,10)
	for player in players:
		p_dic={}
		p_dic['rank']=cnt
		p_dic['name']=player[0]
		p_dic['goal']=player[1]
		rank_list.append(p_dic)
		cnt+=1
	return rank_list

def add_player(data):
	player = Player(
		email 	 = data['email'],
		player_name = data['username'],
		major	 = data['major'],
		student_id = data['student_id'],
		college	= data['college'],
		password = db.func.md5(data['password']),
		phone	 = data['phone'],
		birthday = data['birthday'],
		role	 = data['role'],
		position 	= data['position'],
		wildcard	= data['wildcard']
	)
	db.session.add(player)
	db.session.commit()
	# logging.debug(player.pk)
	return player.pk

def add_player_with_uniform_num(data):
	player = Player(
		email 	 = data['email'],
		player_name = data['username'],
		major	 = data['major'],
		student_id = data['student_id'],
		college	= data['college'],
		password = db.func.md5(data['password']),
		phone	 = data['phone'],
		birthday = data['birthday'],
		role	 = data['role'],
		position 	= data['position'],
		uniform_number	= data['uniform_number'],
		wildcard = data['wildcard']
	)	
	db.session.add(player)
	db.session.commit()
	return player.pk

def add_profile_image(user_pk, filename):
	user= get_player(user_pk)
	user.profile_img =filename
	db.session.commit()

def edit_player(player_pk, data):
	player=Player.query.get(player_pk)
	player.birthday=data['birthday']
	player.college=data['college']
	player.major=data['major']
	player.phone=data['phone']
	player.role=data['role']
	player.position=data['position']
	player.wildcard=data['wildcard']
	if data['uniform_number']!="":
		player.uniform_number=data['uniform_number']
	else:
		player.uniform_number= sql.null()
	if player.password==db.func.md5(data['password']):
		player.password.flush()
		player.password=db.func.md5(data['password'])
	else:
		player.password=db.func.md5(data['password'])
	db.session.commit()


def search_player_pk_by_player_name(name):
	pk_list=[]
	for i in Player.query.filter(Player.player_name.like('%' + name + '%')).with_entities(Player.pk).all():
		pk_list.append(i[0])
	return pk_list

def get_player_list(email):
	player=Player.query.filter_by(email=email).first()
	return player

def get_player(pk):
	return Player.query.get(pk)

def get_status(pk):
	return Status.query.get(pk).status

def login_check(email,password):
	return Player.query.filter(Player.email==email,Player.password==db.func.md5(password)).count()!=0

def login_player(email,password):
	return Player.query.filter(Player.email==email,Player.password==db.func.md5(password)).first()

def get_player_pk_by_player_name(name):
   pk_list=[]
   for i in Player.query.filter_by(player_name=name).with_entities(Player.pk).all():
      pk_list.append(i[0])
   return pk_list

def return_captain_pk_by_team_pk(team_pk):
	# captain_pk=Player.query.filter_by(team_pk=team_pk, role="Captain").with_entities(Player.pk).first()
	# return captain_pk[0]
	return Player.query.filter(and_(Player.role=="Captain", Player.team_pk==team_pk)).with_entities(Player.pk).all()

def register_team_pk(player_pk, team_pk):
	player=Player.query.get(player_pk)
	player.team_pk=team_pk
	db.session.commit()

def input_yellow_card(player_pk,cnt):
	player=Player.query.get(player_pk)
	player.yellow_card_count=player.yellow_card_count+cnt
	player.limit_count=player.limit_count+cnt
	db.session.commit()

def input_red_card(player_pk):
	player=Player.query.get(player_pk)
	player.red_card_count=player.red_card_count+1
	#출전경기 2경기제한
	player.limit_of_participation=player.limit_of_participation+2
	db.session.commit()

def if_limit_count_3(player_pk):
#y카드 3번받을때 출전제한 한번 증가시키고 다시 리셋
	player=Player.query.get(player_pk)
	if player.limit_count==3:
		player.limit_count=0
		player.limit_of_participation=player.limit_of_participation+1
		limitation_notification(player_pk)
		db.session.commit()

def id_generator(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def find_user(text):
	user = Player.query.filter(Player.player_name.like('%'+text+'%')).all()
	return user

def plus_match_count_for_player(pk):
	player=Player.query.filter_by(pk=pk).first()
	player.match_count=player.match_count+1
	db.session.commit()