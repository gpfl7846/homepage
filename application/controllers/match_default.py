#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from application.models.schema import *
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.round_manager import *
from datetime import datetime

@app.route('/match_default',defaults={'round':None})
@app.route('/match_default/<int:round>')
def match_default(round):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	if round==None:
		now_round=get_next_match()
		if match_by_date(now_round)!=None:
			home=match_by_date(now_round)
			check="true"
		else:
			home=[]
			message="false"
		if (now_round+1)!=10:
			home_next=match_by_date(now_round+1)
			message="true"
		else:
			home_next=[]
			message="false"
		return render_template('match_default.html',check=check, message=message, home=home, home_next=home_next,now_round=now_round,now_next_round=now_round+1)

	else:
		#match_by_default_by_round
		r=get_round_by_season_and_league(round,2014, 2)
		reviews= Round.query.get(r.pk).reviews
		return render_template('match_default.html', r=r, reviews=reviews)

@app.route('/round_input/<int:round>')
def round_input(round):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	match_list=get_match_list_by_round(round,2014,2)
	round_output=[]
	for match in match_list:
		round_output.append(get_match_result_by_match_pk(match.pk))
	return render_template("jaehee.html",round_output=round_output)

@app.route('/match_by_date/<int:round>')
def match_by_date(round):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	match_list=get_match_list_by_round(round,2014,2)
	round_output=[]
	for match in match_list:
		result={}
		result['date']=Match.query.filter_by(pk=match).with_entities(Match.date).first()[0]
		result['match_result']=get_match_result_by_match_pk(match)
		round_output.append(result)
	return round_output

# @app.route('/season_match_by_date')
# def season_match_by_date():
# 	match_list=get_match_list_by_round(round,2014,1)
# 	season_output=[]
# 	for match in match_list:
# 		season_output.append(get_match_result_by_match_pk(match))
# 	return render_template("jaehee.html",season_output=season_output)

@app.route('/next_matches')
def next_matches():
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	match_list=get_match_list_by_round(get_next_match(),2014,2)
	next_round_output=[]
	for match in match_list:
		next_round_output.append(get_match_result_by_match_pk(match))
	return next_round_output

@app.route('/where_to_go/<int:match_pk>')
def where_to_go(match_pk):
	if 'logged_in' not in session:
		return redirect(url_for('index'))

	match_inst = get_match_by_match_pk(match_pk)
	match_date = match_inst.date
	date_now = datetime.now()
	test = match_date < date_now
	if match_date < date_now:
		return redirect(url_for('after_match', match_pk=match_pk))
	elif match_date > date_now:
		return redirect(url_for('before_match', match_pk=match_pk))
	

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404