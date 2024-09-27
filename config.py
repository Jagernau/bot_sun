from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN=config['TOKEN']

DB_HOST=config['DB_HOST']
MYSQL_USER=config['MYSQL_USER']
MYSQL_DB_NAME=config['MYSQL_DB_NAME']
MYSQL_PASSWORD=config['MYSQL_PASSWORD']
MYSQL_PORT=config['MYSQL_PORT']

connection_mysql = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{DB_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}"
