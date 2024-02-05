from flask import Flask, request, jsonify, Blueprint
from app import app
from app import db
from app.utils import *
from sqlalchemy.sql.expression import text
import cx_Oracle


terms_bp = Blueprint('terms', __name__)


connection = None

connection = cx_Oracle.connect('ADMIN/ADMIN@192.168.0.47:1521/xe')

# connection = cx_Oracle.connect('DBTEST/DBTEST@localhost:1521/xe')
    
cursor = connection.cursor()



# 데이터베이스 테스트 응답
@app.route('/api/name', methods=['POST'])
def db_name():
    body = request.get_json()
    user_utterance = body['userRequest']['utterance']

    # 데이터베이스 쿼리 수행
    cursor.execute(f"SELECT TERMS_NAME, TERMS_DETAIL FROM TBL_TERMS WHERE TERMS_NAME = '{user_utterance}'") 
    data = cursor.fetchall()

    outputs = []

    for row in data:
        terms_name, terms_detail = row
        print(f"TERMS_NAME: {terms_name}, TERMS_DETAIL: {terms_detail}")

    
    responseBody = {
  "version": "2.0",
  "template": {
    "outputs": [
      {
        "textCard": {
          "title": f"{terms_name}",
          "description": f"{terms_detail}"
        }
      }
    ]
  }
}

    return responseBody


# 데이터베이스 테스트 응답
@app.route('/api/category', methods=['POST'])
def db_category():
    body = request.get_json()
    user_utterance = body['userRequest']['utterance']

    # 페이지 정보 가져오기
    page = int(body.get('page', 1))  # 기본값은 1
    page_size = 5

    # 데이터베이스 쿼리 수행 (페이지 기능 추가)
    offset = (page - 1) * page_size
    limit = page * page_size

    cursor.execute(f"""
        SELECT * FROM (
            SELECT a.*, ROWNUM rnum FROM (
                SELECT TERMS_NAME, TERMS_DETAIL
                FROM TBL_TERMS
                WHERE TERMS_CATEGORY = '{user_utterance}'
            ) a
            WHERE ROWNUM <= {limit}
        )
        WHERE rnum > {offset}
    """)

    data = cursor.fetchall()

    outputs = []

    for row in data:
        terms_name, terms_detail, additional_column = row
        print(f"TERMS_NAME: {terms_name}, TERMS_DETAIL: {terms_detail}")

        output = {
        "textCard": {
            "title": f"{terms_name}",
            "description": f"{terms_detail}"
        }
    }

        outputs.append(output)

    # 전체 페이지 수 계산
    total_count = cursor.execute(f"SELECT COUNT(*) FROM TBL_TERMS WHERE TERMS_CATEGORY = '{user_utterance}'").fetchone()[0]
    total_pages = (total_count + page_size - 1) // page_size

    # 응답 데이터에 페이지 정보 추가
    response = {
        "version": "2.0",
        "template": {
            "outputs": outputs
        },
        "page": page,
        "totalPages": total_pages
    }

    return jsonify(response)



# 데이터베이스 테스트 응답
@app.route('/api/random_terms', methods=['POST'])
def random_terms():
    body = request.get_json()
    user_utterance = body['userRequest']['utterance']

    # '시작'이라는 문장이 아닌 경우 처리
    if user_utterance != '시작':
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "해당 기능은 '시작'이라는 문장에서만 실행됩니다."
                        }
                    }
                ]
            }
        }
        return jsonify(response)

    # 데이터베이스 쿼리 수행 (랜덤으로 5개 선택)
    cursor.execute(f"""
        SELECT TERMS_NAME, TERMS_DETAIL
        FROM TBL_TERMS
        ORDER BY DBMS_RANDOM.VALUE
    """)
    
    data = cursor.fetchmany(5)

    outputs = []

    for row in data:
        terms_name, terms_detail = row
        print(f"TERMS_NAME: {terms_name}, TERMS_DETAIL: {terms_detail}")

        output = {
        "textCard": {
            "title": f"{terms_name}",
            "description": f"{terms_detail}"
        }
    }

        outputs.append(output)

    # 응답 데이터 구성
    response = {
        "version": "2.0",
        "template": {
            "outputs": outputs
        }
    }

    return jsonify(response)