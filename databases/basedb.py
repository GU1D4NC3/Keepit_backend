from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
account = config["account"]

DB_URL = f'mysql+pymysql://{account["db_user"]}:{account["db_password"]}@{account["db_host"]}:{account["db_port"]}/{account["db_scheme"]}'


class EngineConn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
