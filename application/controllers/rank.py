#-*- coding:utf-8 -*-
from application import app
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template, flash
from application import db
from application.models.schema import *
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.player_manager import *
import logging

@app.route('/rank')
def rank():
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    test_test=get_player_list_by_league(2)
    team_rank_list=get_rank_team_list(2)
    
    return render_template('rank_test.html',test_test=test_test,team_rank_list=team_rank_list)