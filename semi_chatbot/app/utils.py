from app.models import *
from sqlalchemy.sql.expression import text

def get_find(user):
    
    find = FIND_REAL_ESTATE.query.filter(FIND_REAL_ESTATE.FIND_GU == user).order_by(text('DBMS_RANDOM.VALUE')).limit(3).all()
   
    # find = TABLE1.query.filter(TABLE1.FIND_GU == user).order_by(text('DBMS_RANDOM.VALUE')).limit(3).all()
    print(find)
    return find

def get_find_dong(user):
    
    find = FIND_REAL_ESTATE.query.filter(FIND_REAL_ESTATE.FIND_DONG == user).order_by(text('DBMS_RANDOM.VALUE')).limit(3).all()

    print(find)
    return find

def sales_gu_find(user):
    
    sales_gu = TBL_SALES.query.filter(TBL_SALES.SALES_GU == user).order_by(text('DBMS_RANDOM.VALUE')).limit(5).all()
    
    
    return sales_gu

def sales_dong_find(user):
    
    sales_dong = TBL_SALES.query.filter(TBL_SALES.SALES_DONG == user).order_by(text('DBMS_RANDOM.VALUE')).limit(3).all()
    print(sales_dong)
    
    return sales_dong

def sales_find_rent(user):
    find = TBL_SALES.query.filter(
        TBL_SALES.SALES_DIVISION == '월세',
        TBL_SALES.SALES_DEPOSIT < user
    ).order_by(text('DBMS_RANDOM.VALUE')).limit(3).all()
    
    return find

def sales_find(user):
    find = TBL_SALES.query.filter(
        TBL_SALES.SALES_DIVISION == '전세',
        TBL_SALES.SALES_DEPOSIT < user
    ).order_by(text('DBMS_RANDOM.VALUE')).limit(3).all()
    
    return find

def quiz_bottom(user):
    quiz = TBL_QUIZ.query.filter(
        TBL_QUIZ.QUIZ_LEVEL == user  
    ).order_by(text('DBMS_RANDOM.VALUE')).limit(1).first()