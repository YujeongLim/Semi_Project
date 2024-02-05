from app import app
from flask import Blueprint,jsonify,request
from app.utils import *


sales_bp = Blueprint('sales', __name__)

@app.route('/api/sales_gu', methods=['POST'])
def sales_gu():
    body = request.get_json()
    print(body)
    
    user = body['userRequest']['utterance']
    
    data = sales_gu_find(user)
    outputs = []
    
        
    for row in data:
            SALES_NAME = row.SALES_NAME 
            SALES_FLOOR = row.SALES_FLOOR 
            SALES_DEPOSIT = row.SALES_DEPOSIT 
            SALES_RENT = row.SALES_RENT 
            SALES_DIVISION = row.SALES_DIVISION
            output={
                "textCard": {
                "title": f"{SALES_NAME}",
                "description": f"{SALES_FLOOR}층 구분 : {SALES_DIVISION} 보증금 :{SALES_DEPOSIT} 월세 :{SALES_RENT}"
            }}
            outputs.append(output)

    
    responseBody = {   
        "version": "2.0",
            "template": {
                "outputs": outputs
                    }
                }
    return jsonify(responseBody)


@app.route('/api/find_sales_rent', methods=['POST'])
def find_sales():
    body = request.get_json()
    print(body)
    
    user = body['userRequest']['utterance']
    
    
    data = sales_find_rent(user)
    
    outputs = []
    
        
    for row in data:
            SALES_NAME = row.SALES_NAME 
            SALES_FLOOR = row.SALES_FLOOR 
            SALES_DEPOSIT = row.SALES_DEPOSIT 
            SALES_RENT = row.SALES_RENT 
            SALES_DIVISION = row.SALES_DIVISION
            output={
                "textCard": {
                "title": f"{SALES_NAME}",
                "description": f"{SALES_FLOOR}층 구분 : {SALES_DIVISION} 보증금 :{SALES_DEPOSIT} 월세 :{SALES_RENT}"
            }}
            outputs.append(output)

    
    responseBody = {   
        "version": "2.0",
            "template": {
                "outputs": outputs
                    }
                }
    return jsonify(responseBody)


@app.route('/api/find_sales', methods=['POST'])
def find_sales_jeonse():
    body = request.get_json()
    print(body)
    
    user = body['userRequest']['utterance']
    
    
    data = sales_find(user)
    
    outputs = []
    
        
    for row in data:
            SALES_NAME = row.SALES_NAME 
            SALES_FLOOR = row.SALES_FLOOR 
            SALES_DEPOSIT = row.SALES_DEPOSIT 
            SALES_RENT = row.SALES_RENT 
            SALES_DIVISION = row.SALES_DIVISION
            output={
                "textCard": {
                "title": f"{SALES_NAME}",
                "description": f"{SALES_FLOOR}층 구분 : {SALES_DIVISION} 보증금 :{SALES_DEPOSIT} 월세 :{SALES_RENT}"
            }}
            outputs.append(output)

    
    responseBody = {   
        "version": "2.0",
            "template": {
                "outputs": outputs
                    }
                }
    return jsonify(responseBody)

