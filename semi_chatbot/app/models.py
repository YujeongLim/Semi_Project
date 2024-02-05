from app import db

class FIND_REAL_ESTATE(db.Model):
    FIND_NO = db.Column(db.Integer, primary_key=True)
    FIND_GU = db.Column(db.String(255), nullable=False)
    FIND_DONG = db.Column(db.String(255), nullable=False)
    FIND_ADDRESS = db.Column(db.String(255), nullable=False)
    FIND_NAME = db.Column(db.String(255))
    FIND_PHONE = db.Column(db.String(255))

class TBL_SALES(db.Model):
    SALES_NO = db.Column(db.Integer, primary_key=True)
    SALES_GU = db.Column(db.String(255), nullable=False)
    SALES_DONG = db.Column(db.String(255), nullable=False)
    SALES_FLOOR = db.Column(db.String(255), nullable=False)
    SALES_DIVISION = db.Column(db.String(255))
    SALES_AREA = db.Column(db.String(255))
    SALES_DEPOSIT = db.Column(db.Integer)
    SALES_RENT = db.Column(db.Integer)
    SALES_NAME = db.Column(db.String(255))
    SALES_CLASS = db.Column(db.String(255))
    
    
class TBL_QUIZ(db.Model):
    QUIZ_ID = db.Column(db.Integer, primary_key=True)
    QUIZ_LEVEL = db.Column(db.String(20), nullable=False)
    QUIZ_WORD = db.Column(db.String(100), nullable=False)
    QUIZ_CONTENT = db.Column(db.Text, nullable=False)