from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

api = Api(prefix="/api/v1")

Base = declarative_base()

db = SQLAlchemy(model_class=Base)
