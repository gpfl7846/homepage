#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from application.models.notification_manager import *
from application.models.player_manager import *
from datetime import datetime, timedelta
from sqlalchemy import or_, and_,sql
# print datetime.now() + timedelta(days=-1)
import logging
from threading import *
import time

@app.route('/notification')
def notification():
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    return render_template("notification.html")

@app.route('/notification_modal/<int:notification_pk>')
def notification_modal(notification_pk):
    if 'logged_in' not in session:
        return redirect(url_for('index'))
        
    return render_template("notification_modal.html")

@app.route('/free_limitation_notification/<int:player_pk>')
def free_limitation_notification(player_pk):
	n_pk=add_notification(19,577,player_pk)
	create_message_and_title(n_pk)
	return None

@app.route('/limitation_notifiation/<int:player_pk>')
def limitation_notification(player_pk):
	#577은 committee의 pk임
	n_pk=add_notification(18,577,player_pk)
	create_message_and_title(n_pk)
	limitation_num=Player.query.filter_by(pk=player_pk).with_entities(Player.limit_of_participation).first()
	set_message(n_pk,limitation_num[0])
	return None

@app.route('/register_match_notification/<int:committee_pk>/<int:match_pk>/<int:team_pk1>/<int:team_pk2>')
def register_match_notification(committee_pk ,match_pk, team_pk1, team_pk2):
	match_noti_for_captains(match_pk,7,team_pk1, committee_pk)
	match_noti_for_captains(match_pk,7,team_pk2, committee_pk)
	return None

@app.route('/register_referee_team_notification/<int:match_pk>/<int:team_pk>/<int:committee_pk>')
def register_referee_team_notification(match_pk, team_pk, committee_pk):
	match_noti_for_captains(match_pk,10,team_pk, committee_pk)
	return None

@app.route('/register_referees/<int:match_pk>/<int:committee_pk>/<int:referee_pk>')
def register_referees(match_pk, committee_pk, referee_pk):
	n_pk=match_add_notification(11, committee_pk, referee_pk, match_pk)
	create_message_and_title(n_pk)
	return None

@app.route('/lineup_notification/<int:match_pk>/<int:player_pk>/<int:captain_pk>')
def lineup_notification(match_pk, player_pk, captain_pk):
	n_pk=match_add_notification(4, captain_pk, player_pk, match_pk)
	create_message_and_title(n_pk)
	return None

#라인업등록시 자기말고 다른주장한테 알려줌
@app.route('/lineup_notification_for_captains/<int:match_pk>/<int:captain_pk>')
def lineup_notification_for_captains(match_pk, captain_pk):
	team_pk=Player.query.filter_by(pk=captain_pk).with_entities(Player.team_pk).first()
	captains=Player.query.filter(and_(Player.role=="Captain", Player.team_pk==team_pk[0], Player.pk!=captain_pk)).with_entities(Player.pk).all()
	for captain in captains:
		# logging.debug(captain[0])
		n_pk=match_add_notification(17, captain_pk, captain[0], match_pk)
		create_message_and_title(n_pk)
	return None

@app.route('/signup_notification/<int:team_pk>/<int:player_pk>')
def signup_notification(team_pk,player_pk):
	captain_list=[]
	# captains=return_captain_pk_by_team_pk(team_pk)
	captains=Player.query.filter(and_(Player.role=="Captain", Player.team_pk==team_pk)).with_entities(Player.pk).all()
	for captain in captains:
		captain_list.append(captain[0])
#2.알림 맨첫번쨰꺼를 생성하고 첫번쨰의 pk가 key값으로 만들어
	n_first=add_notification(1,player_pk,captain_list[0])
	create_message_and_title(n_first)
	set_key(n_first,n_first)
#3.나머지 꺼도 알람 만들고 2번에서 만들었던 pk를 key로 set
	for captain_pk in captain_list[1:]:
		n_pk=add_notification(1,player_pk,captain_pk)
		create_message_and_title(n_pk)
		set_key(n_pk,n_first)
	return None

@app.route('/confirm_match_result_notification/<int:match_pk>')
def confirm_match_result_notification(match_pk):
	#운영위원회 pk를 어떻게 넣을 것인가?
	n_pk=match_add_notification(13, session['user_pk'], 577, match_pk)
	create_message_and_title(n_pk)
	return None

@app.route('/notification_confirm/<int:notification_pk>/<int:result>/<int:type>')
def notification_confirm(notification_pk, result, type):
	confirm_notification(notification_pk,result)
	notification=Notification.query.filter_by(pk=notification_pk).with_entities(Notification.sender_pk, Notification.receiver_pk,Notification.match_pk).first()
	if type==1:
		if result==1:
			team_pk=Player.query.filter_by(pk=notification[1]).with_entities(Player.team_pk).first()
			# logging.debug(team_pk[0])
			register_team_pk(notification[0],team_pk[0])
			new_notification=add_notification(2,notification[1],notification[0])
			create_message_and_title(new_notification)
			delete_repetition_notification(Notification.query.filter_by(pk=notification_pk).with_entities(Notification.key).first()[0])#
		else:
			new_notification=add_notification(3,notification[1],notification[0])
			create_message_and_title(new_notification)
			delete_repetition_notification(Notification.query.filter_by(pk=notification_pk).with_entities(Notification.key).first()[0])#

	if type==4: #라인업등록메세지 선수에게 갔을 때
		team_pk=Player.query.filter_by(pk=notification[1]).with_entities(Player.team_pk).first()
		if result==1: #선수가 승인
			noti_for_captains(5,team_pk[0],notification[1])
			plus_match_count_for_player(notification[1])
		else: #선수가 거절 -> 디비에서 삭제
			noti_for_captains(6,team_pk[0],notification[1])
			delete_match_player(notification[2], notification[1])

	if type==7: #경기등록 메세지 주장에게 가면
		match_pk=Notification.query.filter_by(pk=notification_pk).with_entities(Notification.match_pk).first()
		if result==1: #주장이 승인하면 운영위원회한테 확인했다는메세지감
			new_notification=match_add_notification(8, notification[1], notification[0], match_pk[0])
			create_message_and_title(new_notification)
			delete_repetition_notification(Notification.query.filter_by(pk=notification_pk).with_entities(Notification.key).first()[0])#
		# team_player선수테이블에 추가		
	if type==10:
		delete_repetition_notification(Notification.query.filter_by(pk=notification_pk).with_entities(Notification.key).first()[0])#
	if type==11: #심판들이 너 심판진으로 등록되었다고 메세지 받으면
		if result==1:
			match_pk=Notification.query.filter_by(pk=notification_pk).with_entities(Notification.match_pk).first()
			new_notification=match_add_notification(12, notification[1], notification[0], match_pk[0])
			create_message_and_title(new_notification)
	if type==13: #운영위원회가 경기결과 확인하면
		match_pk=Notification.query.filter_by(pk=notification_pk).with_entities(Notification.match_pk).first()
		if result==1: #올바른 경기결과.
			new_notification=match_add_notification(14, notification[1], notification[0], match_pk[0])
			create_message_and_title(new_notification)
		else: #심판한테 다시 입력하라 알릴경우
			new_notification=match_add_notification(15, notification[1], notification[0], match_pk[0])
			create_message_and_title(new_notification)
			#이 단계에 경기결과 입력한거 삭제하는 함수.
	return redirect(url_for('my_notification', user_pk=session['user_pk']))

@app.route('/my_notification/<int:user_pk>')
def my_notification(user_pk):
	# logging.debug(count_notification(user_pk))
	notification_list=[]
	notifications=check_my_notification(user_pk)
	for noti in notifications:
		notification=Notification.query.get(noti.pk)
		player_info=Player.query.filter_by(pk=notification.sender_pk).with_entities(Player.player_name,Player.team_pk).first()
		n_dic={'match':'','message':''}
		if player_info[1]!=None:
			player_team=Team.query.filter_by(pk=player_info[1]).with_entities(Team.name).first()
			n_dic['sender_team']=player_team[0]
		# logging.debug(notification[0])
		# logging.debug(notification[1])
		n_dic['pk']=notification.pk
		n_dic['title']=notification.title
		n_dic['sender_name']=player_info[0]
		n_dic['type']=notification.type_pk
		if notification.type_pk==4 or notification.type_pk==7 or notification.type_pk==9 or notification.type_pk==10 or notification.type_pk==11 or notification.type_pk==12 or notification.type_pk==13 or notification.type_pk==14 or notification.type_pk==15 or notification.type_pk==16 or notification.type_pk==17:
			n_dic['match']=notification.match
		if notification.type_pk==18:
			n_dic['message']=notification.message
		notification_list.append(n_dic)
	for noti in notification_list:
		if noti['type']==2 or noti['type']==3 or noti['type']==5 or noti['type']==6 or noti['type']==8 or noti['type']==9 or noti['type']==12:
			confirm_notification(noti['pk'],1)

	return render_template('notification.html',notification_list=notification_list)

@app.route('/get_match_info/<int:match_pk>')
def get_match_info(match_pk):
	return Match.query.filter_by(pk=match_pk).with_entities(Match.date)[0]

@app.route('/match_notification_before_2day/<int:match_pk>')
def match_notification_before_2day(match_pk):
	teams=Match.query.filter_by(pk=match_pk).first().match_teams
	# team_pk_list=[]
	# for team in teams:
	# 	team_pk_list.append(team.team.pk)
	team_pk1=teams[0].team.pk
	team_pk2=teams[1].team.pk
	match_noti_for_captains(match_pk,9,team_pk1, 577)
	match_noti_for_captains(match_pk,9,team_pk2, 577)
	return None

@app.route('/request_match_result_notification/<int:match_pk>/<int:referee_pk>')
def request_match_result_notification(match_pk, referee_pk):
	n_pk=match_add_notification(16, 577, referee_pk, match_pk)
	create_message_and_title(n_pk)
	return None

#여러명의 주장에게 알람 보내는 함수
@app.route('/noti_for_captains/<int:type>/<int:team_pk>/<int:sender_pk>')
def noti_for_captains(type,team_pk,sender_pk):
#1.captain인애들 pk 리스트로 만들어
	captain_list=[]
	captains=Player.query.filter(and_(Player.role=="Captain", Player.team_pk==team_pk)).with_entities(Player.pk).all()
	for captain in captains:
		captain_list.append(captain[0])
#2.알림 맨첫번쨰꺼를 생성하고 첫번쨰의 pk가 key값으로 만들어
	n_first=add_notification(type,sender_pk,captain_list[0])
	create_message_and_title(n_first)
	set_key(n_first,n_first)
#3.나머지 꺼도 알람 만들고 2번에서 만들었던 pk를 key로 set
	for i in captain_list[1:]:
		n_pk=add_notification(type,sender_pk,i)
		create_message_and_title(n_pk)
		set_key(n_pk,n_first)
	return None

#여러명의 주장에게 알람 보내는 함수
@app.route('/match_noti_for_captains/<int:match_pk>/<int:type>/<int:team_pk>/<int:sender_pk>')
def match_noti_for_captains(match_pk,type,team_pk,sender_pk):
#1.captain인애들 pk 리스트로 만들어
	captain_list=[]
	captains=Player.query.filter(and_(Player.role=="Captain", Player.team_pk==team_pk)).with_entities(Player.pk).all()
	for captain in captains:
		captain_list.append(captain[0])
#2.알림 맨첫번쨰꺼를 생성하고 첫번쨰의 pk가 key값으로 만들어
	n_first=match_add_notification(type,sender_pk,captain_list[0],match_pk)
	create_message_and_title(n_first)
	set_key(n_first,n_first)
#3.나머지 꺼도 알람 만들고 2번에서 만들었던 pk를 key로 set
	for i in captain_list[1:]:
		n_pk=match_add_notification(type,sender_pk,i,match_pk)
		create_message_and_title(n_pk)
		set_key(n_pk,n_first)
	return None

#주장중에 한명이 확인하면 나머지 같은 key를 가지고 confirm이 null인 알림들을 삭제
@app.route('/delete_repetition_notification/<int:n_key>')
def delete_repetition_notification(n_key):
	n_list=Notification.query.filter(and_(Notification.confirm==None, Notification.key==n_key)).with_entities(Notification.pk).all()
	for n in n_list:
		delete_notification(n[0])
	return None