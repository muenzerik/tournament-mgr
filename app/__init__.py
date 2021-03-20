import logging

from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

import re

app = Flask(__name__)
app.config.from_object(Config)

#allocate the database objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/maennerfestspiele', echo=True)

if not database_exists(engine.url):
    logging.info('Database does not exist. Will Create one...')
    create_database(engine.url)  

    with open('db/schema/tournament-mgr.sql') as file:
        print("\n[INFO] Executing SQL script file: '%s'", file)
        statement = ""

        for line in file:
            valid = False
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if re.match(r'^\n', line):  # ignore empty lines
                continue
            if (not re.search(r';$', line) and line.find(';') == -1):  # keep appending lines that don't end in ';'
                statement = statement + line
            if line.find(';') > 0: # but only if there are not multi statements in a line
                line = line.split(';', 1)[0]
                statement = statement + line
                statement = statement + ';'
                if statement.find('BEGIN') > 0:
                    if statement.find('END;$$;') > 0: #handle function blocks
                        valid = True
                else:
                    valid = True              
            if valid == True:
                print("\n\n[DEBUG] Executing SQL statement:\n%s", (statement))
                try:
                    engine.execute(statement)
                except (SQLAlchemyError) as e:
                    print("\n[WARN] SQLError during execute statement \n\tArgs: '%s'", str(e.args))
                statement = ""

    logging.info('...done')

from app import routes
