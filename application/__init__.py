from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.debugtoolbar import DebugToolbarExtension

# migrate
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

# Create Flask Application Instance
app = Flask('application')

# Import application configuration file
import config

db = SQLAlchemy(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True

from application.models import schema

# Import Every function in 'controllers' directory
for base, dirs, names in os.walk(os.path.join('application', 'controllers')):
	for name in filter(lambda s: s.endswith('.py') and s != '__init__.py', names) :
		exec('from application.controllers.'+name[:-3]+' import *')

