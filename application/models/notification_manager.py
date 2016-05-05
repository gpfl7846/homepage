#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from sqlalchemy import or_, and_,sql
import datetime
import logging

def get_notification_by_pk(pk):
	return Notification.query.get(pk)

# def read_notification(n_pk):
# 	notification=Notification.query.get(n_pk)
# 	notification.read=1
# 	db.session.commit()

def add_notification(type, sender_pk, receiver_pk):
	notification = Notification(
	type_pk=type,
	sender_pk=sender_pk,
	receiver_pk=receiver_pk
		)
	db.session.add(notification)
	db.session.commit()
	return notification.pk

def match_add_notification(type, sender_pk, receiver_pk, match_pk):
	notification = Notification(
	type_pk=type,
	sender_pk=sender_pk,
	receiver_pk=receiver_pk,
	match_pk=match_pk
		)
	db.session.add(notification)
	db.session.commit()
	return notification.pk

def create_message_and_title(pk):
# 경기정보에 대한 타입이면 메세지에 경기정보를 불러와서 추가해주고 그에 대한 링크도 걸어줘야함. 클릭했을 떄 바로 이동하도록
	notification=get_notification_by_pk(pk)
	if notification.type_pk==1:
		notification.title="선수승인 요청"
		notification.message="새로 가입한 선수승인을 요청했습니다."
	if notification.type_pk==2:
		notification.title="등록되었습니다."
	if notification.type_pk==3:
		notification.title="등록되지 않았습니다."
	if notification.type_pk==4:
		notification.title="경기에 출전 선수로 등록되었습니다."
	if notification.type_pk==5:
		notification.title="선수가 라인업을 승인하였습니다."
	if notification.type_pk==6:
		notification.title="선수가 라인업을 거절하였습니다. 다시 라인업을 추가하세요."
	if notification.type_pk==7:
		notification.title="경기가 등록되었습니다."
	if notification.type_pk==8:
		notification.title="주장이 확인했습니다."
	if notification.type_pk==9:
		notification.title="2일 뒤에 경기가 있습니다."
	if notification.type_pk==10:
		notification.title="경기에 심판팀으로 등록되었습니다. 심판을 등록하세요."
	if notification.type_pk==11:
		notification.title="경기에 심판진으로 등록되었습니다. 확인을 눌러주세요."
	if notification.type_pk==12:
		notification.title="심판이 확인을 완료했습니다."
	if notification.type_pk==13:
		notification.title="심판이 경기결과를 입력했습니다.운영위원회의 승인이 필요합니다."
	if notification.type_pk==14:
		notification.title="경기결과를 운영진이 승인했습니다."
	if notification.type_pk==15:
		notification.title="경기결과에 대해 운영진이 승인하지 않았습니다. 경기결과 수정이 필요합니다."
	if notification.type_pk==16:
		notification.title="경기가 종료되었으니 심판은 경기결과를 입력해 주십시오."
	if notification.type_pk==17:
		notification.title="주장이 경기 라인업을 등록하였습니다."
	if notification.type_pk==18:
		notification.title="경기동안 출전하실 수 없습니다."
	if notification.type_pk==19:
		notification.title="경기출전제한이 풀렸습니다."
	db.session.commit()

def return_match_pk_by_notification_pk(n_pk):
	notification=get_notification_by_pk(n_pk)
	# if notification.type_pk=="경기관련pk":
	# 	return notification.match_pk
	return notification.match_pk

def check_my_notification(user_pk):
	return Notification.query.filter(Notification.receiver_pk==user_pk, Notification.confirm==None).order_by(db.desc(Notification.send_time)).all()

def confirm_notification(n_pk,result):
	# notification=Notification.query.filter_by(pk=pk).with_entities(Notification.pk).all()
	notification=Notification.query.get(n_pk)
	notification.confirm=result
	# notification.read=1
	notification.confirm_time=datetime.datetime.now()
	db.session.commit()

def read_notification(n_pk):
	notification=Notification.query.get(n_pk)
	notification.read=1
	db.session.commit()

def return_type(type_pk):
	return Notification_type.query.get(type_pk).type

def count_notification(user_pk):
	return Notification.query.filter(Notification.receiver_pk==user_pk, Notification.confirm==None).count()

def delete_notification(n_pk):
	notification=Notification.query.filter_by(pk=n_pk).first()
	db.session.delete(notification)
	db.session.commit()

def set_key(n_pk, key_input):
	notification=Notification.query.get(n_pk)
	notification.key=key_input
	db.session.commit()

def set_message(n_pk, message_input):
	notification=Notification.query.get(n_pk)
	notification.message=message_input
	db.session.commit()	