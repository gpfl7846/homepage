#-*- coding:utf-8 -*-
from flask import render_template, redirect, url_for,session, request
from application import db
from schema import *
from sqlalchemy import or_, and_
from application.models.team_manager import *
import datetime
from sqlalchemy import text, exc, insert

def get_round(round_pk):
	return Round.query.get(round_pk)
