import flask_sqlalchemy
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = f"postgresql+psycopg2://{os.getenv('DB_URI')}"
        if not value:
            raise ValueError("no DB_URI environment variable")
        return value
    
    @property
    def JWT_SECRET_KEY(self):
        value = os.getenv("JWT_SECRET_KEY")
        if not value:
            raise ValueError("no JWT_SECRET_KEY environnment variable")
        return value
        
    @property
    def SECRET_KEY(self):
        value = os.getenv("SECRET_KEY")
        if not value:
            raise ValueError("no SECRET_KEY environnment variable")
        return value
    
    JWT_COOKIE_CSRF_PROTECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    JWT_TOKEN_LOCATION = ['cookies']

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    
env = os.getenv("FLASK_DEV")

if env == "development":
    configuration = DevelopmentConfig()
elif env == "testing":
    configuration = TestingConfig()   
else:
    configuration = ProductionConfig()
