import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('AUTH_POSTGRES_USER',"admin")
POSTGRES_PASSWORD = os.getenv('AUTH_POSTGRES_PASSWORD',"admin1234")
POSTGRES_HOST = os.getenv('AUTH_POSTGRES_HOST',"localhost")
POSTGRES_PORT = os.getenv('AUTH_POSTGRES_PORT',"5433")
POSTGRES_DB = os.getenv('AUTH_POSTGRES_DB',"competition")

class Config:
    PORT = os.getenv('AUTH_PORT', 5001)
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):

    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
