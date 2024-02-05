from flask import Flask, request, jsonify, Blueprint
from app import app
from app.utils import *
from sqlalchemy.sql.expression import text
import cx_Oracle
import json
import random

quiz_bp = Blueprint('quiz', __name__)

# 데이터베이스 연결
connection = cx_Oracle.connect('ADMIN/ADMIN@192.168.0.47:1521/xe')
cursor = connection.cursor()

# LOB 데이터를 문자열로 변환
def lob_to_str(lob_data):
    if isinstance(lob_data, str):
        return lob_data
    elif lob_data:
        return lob_data.read()
    return None

# 사용자별 문제 상태를 저장하는 딕셔너리
user_state = {}

# 카카오톡 텍스트형 응답 - 초급 문제 선택
@app.route('/api/selectBeginner', methods=['POST'])
def select_beginner():
    body = request.get_json()
    user_id = str(body['userRequest']['user']['id'])

    # 데이터베이스에서 '하' 레벨의 퀴즈와 정답 선택
    cursor.execute("SELECT QUIZ_CONTENT, QUIZ_WORD FROM TBL_QUIZ WHERE QUIZ_LEVEL = '하'")
    all_questions_answers = cursor.fetchall()

    if not all_questions_answers:
        return jsonify({"message": "No beginner level quiz available"}), 404

    # 랜덤으로 3개의 문제 선택
    selected_questions = random.sample(all_questions_answers, min(3, len(all_questions_answers)))
    # 첫 번째 문제만 선택
    # selected_questions = [all_questions_answers[0]]
    
    # 사용자 상태 저장
    save_user_state(user_id, selected_questions, 0)

    # 사용자 상태 저장
    result = save_user_state(user_id, selected_questions, 0)
    print("save_user_state 결과:", result)
    
    # 첫 번째 문제와 객관식 답변 출력
    first_question, correct_answer = selected_questions[0]
    other_answers = [qa[1] for qa in all_questions_answers if qa[1] != correct_answer]
    selected_answers = random.sample(other_answers, min(3, len(other_answers)))
    selected_answers.append(correct_answer)
    random.shuffle(selected_answers)

    # 객관식 답변 버튼 생성
    quick_replies = [{"action": "message", "label": ans, "messageText": ans} for ans in selected_answers]

    response_text = f"초급 문제를 선택하셨습니다. 첫 번째 문제입니다:\n'{first_question}'은(는) 무엇일까요?"

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": response_text}}],
            "quickReplies": quick_replies
        }
    }

    return jsonify(responseBody)

# 카카오톡 텍스트형 응답 - 중급 문제 선택
@app.route('/api/selectIntermediate', methods=['POST'])
def select_intermediate():
    body = request.get_json()
    user_id = str(body['userRequest']['user']['id'])

    cursor.execute("SELECT QUIZ_CONTENT, QUIZ_WORD FROM TBL_QUIZ WHERE QUIZ_LEVEL = '중'")
    all_questions_answers = cursor.fetchall()

    if not all_questions_answers:
        return jsonify({"message": "No intermediate level quiz available"}), 404

    selected_questions = random.sample(all_questions_answers, min(3, len(all_questions_answers)))
    # selected_questions = [all_questions_answers[0]] # 첫 번째 문제만 선택

    save_user_state(user_id, selected_questions, 0)
    result = save_user_state(user_id, selected_questions, 0)
    print("save_user_state 결과:", result)
    
    first_question, correct_answer = selected_questions[0]
    other_answers = [qa[1] for qa in all_questions_answers if qa[1] != correct_answer]
    selected_answers = random.sample(other_answers, min(3, len(other_answers)))
    selected_answers.append(correct_answer)
    random.shuffle(selected_answers)

    # 객관식 답변 버튼 생성
    quick_replies = [{"action": "message", "label": ans, "messageText": ans} for ans in selected_answers]

    response_text = f"중급 문제를 선택하셨습니다. 첫 번째 문제입니다:\n'{first_question}'은(는) 무엇일까요?"

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": response_text}}],
            "quickReplies": quick_replies
        }
    }

    return jsonify(responseBody)

# 카카오톡 텍스트형 응답 - 고급 문제 선택
@app.route('/api/selectAdvanced', methods=['POST'])
def select_advanced():
    body = request.get_json()
    user_id = str(body['userRequest']['user']['id'])

    cursor.execute("SELECT QUIZ_CONTENT, QUIZ_WORD FROM TBL_QUIZ WHERE QUIZ_LEVEL = '상'")
    all_questions_answers = cursor.fetchall()

    if not all_questions_answers:
        return jsonify({"message": "No advanced level quiz available"}), 404

    selected_questions = random.sample(all_questions_answers, min(3, len(all_questions_answers)))
    # selected_questions = [all_questions_answers[0]] # 첫 번째 문제만 선택

    save_user_state(user_id, selected_questions, 0)
    result = save_user_state(user_id, selected_questions, 0)
    print("save_user_state 결과:", result)
    
    first_question, correct_answer = selected_questions[0]
    other_answers = [qa[1] for qa in all_questions_answers if qa[1] != correct_answer]
    selected_answers = random.sample(other_answers, min(3, len(other_answers)))
    selected_answers.append(correct_answer)
    random.shuffle(selected_answers)

    # 객관식 답변 버튼 생성
    quick_replies = [{"action": "message", "label": ans, "messageText": ans} for ans in selected_answers]

    response_text = f"고급 문제를 선택하셨습니다. 첫 번째 문제입니다:\n'{first_question}'은(는) 무엇일까요?"

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": response_text}}],
            "quickReplies": quick_replies
        }
    }

    return jsonify(responseBody)

# 사용자 상태 저장
def save_user_state(user_id, questions, current_index):
    # questions 내의 각 항목에 대해 LOB를 문자열로 변환
    questions_str = [
        (lob_to_str(question), lob_to_str(answer))
        for question, answer in questions
    ]

    questions_json = json.dumps(questions_str)
    # 데이터베이스에 사용자 상태 저장
    sql = """
    MERGE INTO user_states u
    USING (
        SELECT :user_id AS user_id, :current_index AS current_index, :questions AS questions FROM dual
    ) incoming
    ON (u.user_id = incoming.user_id)
    WHEN MATCHED THEN
        UPDATE SET u.current_index = incoming.current_index, u.questions = incoming.questions
    WHEN NOT MATCHED THEN
        INSERT (user_id, current_index, questions)
        VALUES (incoming.user_id, incoming.current_index, incoming.questions)
    """

    cursor.execute(sql, user_id=user_id, current_index=current_index, questions=questions_json)
    connection.commit()
    return True  # 데이터베이스 작업이 성공적으로 완료되었음을 나타냄



# 사용자 상태 조회
def get_user_state(user_id):
    user_id_str = str(user_id)
    cursor.execute("SELECT current_index, questions FROM user_states WHERE user_id = :user_id", user_id=user_id_str)
    row = cursor.fetchone()

    if row is None:
        print("No data found for user_id:", user_id)
        return None

    current_index, questions_lob = row
    questions_str = lob_to_str(questions_lob)  # LOB 데이터를 문자열로 변환
    questions = json.loads(questions_str) if questions_str else []
    print("Fetched data:", current_index, questions)
    return {"current_index": current_index, "questions": questions}



# 사용자 답변 처리
@app.route('/api/answerQuestion', methods=['POST'])
def answer_question():
    try:
        body = request.get_json()
        user_request = body['userRequest']
        user_id = str(user_request['user']['id'])
        answer = user_request['utterance'].strip()

        current_state = get_user_state(user_id)
        if current_state is None:
            return jsonify({"message": "세션이 만료되었거나 잘못된 접근입니다."}), 400

        current_index = current_state['current_index']
        current_question, correct_answer = current_state['questions'][current_index]

        # 모든 질문과 답변 불러오기
        cursor.execute("SELECT QUIZ_CONTENT, QUIZ_WORD FROM TBL_QUIZ")
        all_questions_answers = cursor.fetchall()

        if answer.lower() == correct_answer.lower():
            current_state['current_index'] += 1
            save_user_state(user_id, current_state['questions'], current_state['current_index'])

            if current_state['current_index'] >= len(current_state['questions']):
                response_text = "잘하셨습니다! 퀴즈가 모두 끝났습니다! 부동산 용어에 대해 많이 배우셨나요?"
                responseBody = {
                    "version": "2.0",
                    "template": {
                        "outputs": [{"simpleText": {"text": response_text}}],
                        "quickReplies": [
                            {
                                "action": "message",
                                "label": "네! 많이 배웠어요!",
                                "messageText": "네! 많이 배웠어요!"
                            }
                        ]
                    }
                }
            else:
                # 모든 질문과 답변 불러오기
                cursor.execute("SELECT QUIZ_CONTENT, QUIZ_WORD FROM TBL_QUIZ")
                all_questions_answers = cursor.fetchall()

                next_question, next_correct_answer = current_state['questions'][current_state['current_index']]
                other_answers = [qa[1] for qa in all_questions_answers if qa[1] != next_correct_answer]
                selected_answers = random.sample(other_answers, min(3, len(other_answers)))
                selected_answers.append(next_correct_answer)
                random.shuffle(selected_answers)
                next_quick_replies = [{"action": "message", "label": ans, "messageText": ans} for ans in selected_answers]
                response_text = f"정답입니다 ! 다음 문제입니다 ! : \n'{next_question}'은(는) 무엇일까요?"

                responseBody = {"version": "2.0", "template": {"outputs": [{"simpleText": {"text": response_text}}], "quickReplies": next_quick_replies}}
        else:
            # 사용자가 틀린 답변을 선택했을 때의 로직
            response_text = "틀렸습니다. 다시 풀어주세요."

            # 동일한 문제와 보기를 다시 제공
            current_question, correct_answer = current_state['questions'][current_index]
            other_answers = [qa[1] for qa in all_questions_answers if qa[1] != correct_answer]
            selected_answers = random.sample(other_answers, min(3, len(other_answers)))
            selected_answers.append(correct_answer)
            random.shuffle(selected_answers)

            quick_replies = [{"action": "message", "label": ans, "messageText": ans} for ans in selected_answers]

            responseBody = {
                "version": "2.0",
                "template": {
                    "outputs": [{"simpleText": {"text": response_text}}],
                    "quickReplies": quick_replies
                }
            }

    except KeyError as e:
        return jsonify({"message": f"잘못된 요청입니다: {str(e)}"}), 400
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"message": f"서버 내부 오류: {str(e)}"}), 500

    return jsonify(responseBody)






