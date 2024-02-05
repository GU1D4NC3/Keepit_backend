from typing import Optional
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
account = config["account"]

DB_URL = f'mysql+pymysql://{account["db_user"]}:{account["db_password"]}@{account["db_host"]}:{account["db_port"]}/{account["db_scheme"]}'


class Settings(BaseSettings):
    SECRET_KEY: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    CLIENT_ID: Optional[str] = None
    CLIENT_SECRET: Optional[str] = None
    REDIRECT_URL: Optional[str] = None
    AUTH_URL: Optional[str] = None
    TOKEN_URL: Optional[str] = None
    GRANT_TYPE: Optional[str] = None

    class Config:
        env_file = ".env"


class EngineConn:
    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle = 500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn