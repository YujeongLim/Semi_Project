from flask import request, jsonify, Blueprint
from app import app
from app import db
from app.utils import *
from sqlalchemy.sql.expression import text

find_bp = Blueprint('find', __name__)



@app.route('/api/gu_find', methods=['POST'])
def gu_find():
    body = request.get_json()
    print(body)
    
    user = body['userRequest']['utterance']
    
    # sql_query = text("SELECT COLUMN3, COLUMN4, COLUMN2 FROM (SELECT COLUMN3, COLUMN4, COLUMN2 FROM TABLE1 WHERE FIND_GU = :user ORDER BY DBMS_RANDOM.VALUE) WHERE ROWNUM <= 3")
    # result = db.session.execute(sql_query, params={'user': user})

    # data = result.fetchall()
    # print(data)
    
    
    data = get_find(user)
    
    outputs = []
    
    for row in data:
            FIND_NAME = row.FIND_NAME 
            FIND_PHONE = row.FIND_PHONE 
            FIND_ADDRESS = row.FIND_ADDRESS 
            
            output={
                "textCard": {
                "title": f"{FIND_NAME}",
                "description": f"전화번호 : {FIND_PHONE}  주소 : {FIND_ADDRESS}"
            }}
            outputs.append(output)
 

    responseBody = {   
        "version": "2.0",
            "template": {
                "outputs": outputs
                    }
                }

    return jsonify(responseBody)


@app.route('/api/dong_find', methods=['POST'])
def dong_find():
    body = request.get_json()
    print(body)
    
    user = body['userRequest']['utterance']
    
    # sql_query = text("SELECT COLUMN3, COLUMN4, COLUMN2 FROM (SELECT COLUMN3, COLUMN4, COLUMN2 FROM TABLE1 WHERE COLUMN1 = :user ORDER BY DBMS_RANDOM.VALUE) WHERE ROWNUM <= 3")
    # result = db.session.execute(sql_query, params={'user': user})

    # data = result.fetchall()
    # print(data)
    
    data = get_find_dong(user)
    outputs = []
    
    for row in data:
            FIND_NAME = row.FIND_NAME 
            FIND_PHONE = row.FIND_PHONE 
            FIND_ADDRESS = row.FIND_ADDRESS 
            
            output={
                "textCard": {
                "title": f"{FIND_NAME}",
                "description": f"전화번호 : {FIND_PHONE}  주소 : {FIND_ADDRESS}"
            }}
            outputs.append(output)
 

    responseBody = {   
        "version": "2.0",
            "template": {
                "outputs": outputs
                    }
                }

    return jsonify(responseBody)