from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from config import Config

app = Flask(__name__)


app.config.from_object(Config)
db = SQLAlchemy(app)


# from app.main import routes as main_routes
# app.register_blueprint(main_routes.main_bp)

from app.find import routes as find_routes
app.register_blueprint(find_routes.find_bp)

from app.sales import routes as sales_routes
app.register_blueprint(sales_routes.sales_bp)

from app.lease import routes as lease_routes
app.register_blueprint(lease_routes.lease_bp)

from app.quiz import routes as quiz_routes
app.register_blueprint(quiz_routes.quiz_bp)

from app.terms import routes as terms_routes
app.register_blueprint(terms_routes.terms_bp)