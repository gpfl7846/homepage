#-*- coding:utf-8 -*-

from flask import request, render_template, session, redirect, url_for, flash
from application import app
from application.models.team_manager import *
from application.models.match_manager import *
from application.models.file_manager import *

@app.route('/teamdefault')
def teamdefault():
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    league2list = get_team_list_by_league(2)
    return render_template('teamdefault.html', league2list=league2list)

@app.route('/get_teamlogo_image/<filename>')
def get_teamlogo_image(filename):
    if 'logged_in' not in session:
        return redirect(url_for('index'))

    # directory = '/gs/kchamps/img/TeamLogo/'
    new_filename=filename.split('.')[0]
    directory='/gs/kchamps/img/Team/'+str(new_filename)+'/logo/'
    filepath = directory + filename.encode('utf8')
    return read_file(filepath)