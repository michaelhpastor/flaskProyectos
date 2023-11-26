import pymysql
from flask import Flask
from config import MYSQL_CONFIG

def create_app(app: Flask):
    app.config['MYSQL_DATABASE_USER'] = MYSQL_CONFIG['user']
    app.config['MYSQL_DATABASE_PASSWORD'] = MYSQL_CONFIG['password']
    app.config['MYSQL_DATABASE_DB'] = MYSQL_CONFIG['db']
    app.config['MYSQL_DATABASE_HOST'] = MYSQL_CONFIG['host']

    return app

def obtener_conexion():
    return pymysql.connect(
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password'],
        host=MYSQL_CONFIG['host'],
        db=MYSQL_CONFIG['db'],
        cursorclass=pymysql.cursors.DictCursor
    )