#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application.models.player_manager import *
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.file_manager import *

@app.route('/player_page/<int:player_pk>')
def player_page(player_pk):
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    player=get_player(player_pk)
    return render_template('player_test.html',player=player, abilities=player.abilities)

@app.route('/player')
def player():
    if 'logged_in' not in session:
        return redirect(url_for('index'))
        
    return render_template('player_page.html')