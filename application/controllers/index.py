#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from application.models.schema import *
from application.models.match_manager import *
from application.models.notification_manager import *
#mail
import webapp2
from google.appengine.api import mail

@app.route('/test')
def testing() :
	return render_template("test.html")

@app.route('/')
def index() :
    if 'logged_in' in session:
    	notification_count=count_notification(session['user_pk'])
    	league2list = get_team_list_by_league(2)
        return render_template("homepage.html", notification_count=notification_count, league2list=league2list)
    else:
        return render_template("index.html")

@app.route('/feedback',methods=['POST'])
def feedback():
	if request.method=="POST":
		user_address ="support@kchamps.com"
		sender_address = "kchamps.com <dev.kchampsleague@gmail.com>"
		subject = "피드백/오류신고내용입니다."
		user_email=str(session['email'])
		body =request.form['content']+"\n"+u"문의한 사람:"+user_email
		mail.send_mail(sender_address, user_address, subject, body)
		return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404