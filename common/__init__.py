from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_mail import Mail


db = SQLAlchemy()
cache = Cache()
mail = Mail()
