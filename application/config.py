from application import app

app.config.update(dict(
    DEBUG=False,
    SECRET_KEY='development key',
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///k-champs?instance=k-champsleague:kchamps',
    migration_directory = 'migrations'
    ))