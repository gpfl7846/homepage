#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from application.models.schema import *
from application.models.player_manager import *
from application.models.match_manager import *
from application.models.team_manager import *
import logging
import json
import datetime
from datetime import datetime,timedelta

@app.route('/calendar')
def calendar() :
    if 'logged_in' not in session:
        return redirect(url_for('index'))
        
    return render_template("calendar.html")

@app.route('/match_list',methods=['POST'])
def match_list():
    if request.method=='POST':
        today=str(request.form['today'])
        if Match.query.filter(Match.date!="").with_entities(Match.date).first()!=None:
        	# d=Match.query.filter(Match.date!=today).first().date
        	days=Match.query.filter(Match.date!=today).with_entities(Match.pk, Match.date, Match.win_team_pk).all()
        	list=[]
        	for d in days:
        		dic={'win_team_pk':"",'match_team1':"",'match_team1_goal':"",'match_team2':"",'match_team2_goal':""}
        		dic['start_time']=str(d[1]).split(" ")[0]+'T'+str(d[1]).split(" ")[1]
        		endtime=d[1]+timedelta(hours=2)
        		dic['end_time']=str(endtime).split(" ")[0]+'T'+str(endtime).split(" ")[1]
        		dic['match_pk']=d[0]
        		logging.debug(dic['end_time'])
        		team_pk_list=[]
        		for team_pk in Match_team.query.filter_by(match_pk=d[0]).with_entities(Match_team.team_pk).all():
        			team_pk_list.append(team_pk[0])
        		if d[2]!=None:
        			dic['win_team_pk']=d[2]
	        		if get_goal_point_by_match_and_team(d[0],team_pk_list[0])[0]!=None:
		    			dic['match_team1_goal']=get_goal_point_by_match_and_team(d[0],team_pk_list[0])[0]
		    		else:
		    			dic['match_team1_goal']=0
		    		if get_goal_point_by_match_and_team(d[0],team_pk_list[1])[0]!=None:
		    			dic['match_team2_goal']=get_goal_point_by_match_and_team(d[0],team_pk_list[1])[0]
		    		else:
		    			dic['match_team2_goal']=0

    			dic['match_team1']=Team.query.filter_by(pk=team_pk_list[0]).with_entities(Team.name).first()[0]
    			dic['match_team2']=Team.query.filter_by(pk=team_pk_list[1]).with_entities(Team.name).first()[0]
        		list.append(dic)
        	return json.dumps(list)
        else:
            message="not exist"
     
            return message #user not exist

       #  if Match.query.filter(Match.date!="").all()!=None:
       #  	# d=Match.query.filter(Match.date!=today).first().date
       #  	days=Match.query.filter(Match.date!=today).all()
       #  	list=[]
       #  	for d in days:
       #  		dic={'win_team_pk':"",'match_team1':"",'match_team1_goal':"",'match_team2':"",'match_team2_goal':""}
       #  		dic['date']=str(d.date).split(" ")[0]
       #  		dic['match_pk']=d.pk
       #  		team_pk_list=[]
       #  		for team_pk in Match_team.query.filter_by(match_pk=d.pk).with_entities(Match_team.team_pk).all():
       #  			team_pk_list.append(team_pk[0])
       #  		if d.win_team_pk!=None:
       #  			dic['win_team_pk']=d.win_team_pk
	      #   		if get_goal_point_by_match_and_team(d.pk,team_pk_list[0])[0]!=None:
		    	# 		dic['match_team1_goal']=get_goal_point_by_match_and_team(d.pk,team_pk_list[0])[0]
		    	# 	else:
		    	# 		dic['match_team1_goal']=0
		    	# 	if get_goal_point_by_match_and_team(d.pk,team_pk_list[1])[0]!=None:
		    	# 		dic['match_team2_goal']=get_goal_point_by_match_and_team(d.pk,team_pk_list[1])[0]
		    	# 	else:
		    	# 		dic['match_team2_goal']=0

    			# dic['match_team1']=Team.query.filter_by(pk=team_pk_list[0]).with_entities(Team.name).first()[0]
    			# dic['match_team2']=Team.query.filter_by(pk=team_pk_list[1]).with_entities(Team.name).first()[0]
       #  		list.append(dic)
       #  	return json.dumps(list)
       #  else:
       #      message="not exist"
     
       #      return message #user not exist
