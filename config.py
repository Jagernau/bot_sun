from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN=config['TOKEN']

DB_HOST=config['DB_HOST']

POSTGRES_USER=config['POSTGRES_USER']
POSTGRES_DB_NAME=config['POSTGRES_DB_NAME']
POSTGRES_PASSWORD=config['POSTGRES_PASSWORD']
POSTGRES_PORT=config['POSTGRES_PORT']

MYSQL_USER=config['MYSQL_USER']
MYSQL_DB_NAME=config['MYSQL_DB_NAME']
MYSQL_PASSWORD=config['MYSQL_PASSWORD']
MYSQL_PORT=config['MYSQL_PORT']


connection_postgres = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"

connection_mysql = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{DB_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}"
