# # app.py (Flask 서버 코드)

# from flask import jsonify, render_template, request, Blueprint
# import pickle
# import numpy as np
# import os
# from app import app
# import pandas as pd
# lease_bp = Blueprint('lease', __name__)

# # 모델 불러오기
# model_path = os.path.join(app.root_path, 'statics', 'model2.pkl')

# with open(model_path, 'rb') as file:
#     model = pickle.load(file)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     feature_names = ["자치구명", "법정동명", "건물면적", "토지면적", "층", "건축년도", "건물용도"]
    
#     user_inputs = [float(request.form.get(feature)) for feature in feature_names]



    
       

#          # 입력값을 모델에 전달하여 예측
#     predicted_log_price = model.predict(np.array([user_inputs], dtype=np.float64))

#          # 무한대 값이 없는 경우 정수로 변환
#     rounded_predicted_price = int(np.expm1(predicted_log_price[0]))

    
#     return jsonify({"prediction": rounded_predicted_price})

# app.py (Flask 서버 코드)

from flask import Flask, render_template, request, Blueprint, jsonify,make_response
import pickle
import numpy as np
import os
from app import app
import pandas as pd
from sklearn.preprocessing import LabelEncoder

lease_bp = Blueprint('lease', __name__)

# 모델 불러오기
model_path = os.path.join(app.root_path, 'statics', 'model2.pkl')

with open(model_path, 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    feature_names = ["자치구명", "법정동명", "건물면적", "토지면적", "층", "건축년도", "건물용도"]
    
    # 클라이언트에서 전송된 데이터 받기
    user_inputs = [request.form.get(feature) for feature in feature_names]


    user_inputs = [float(x) for x in user_inputs]
    

    # 입력값을 모델에 전달하여 예측
    predicted_log_price = model.predict(np.array([user_inputs], dtype=np.float64))
    print(model)
    # 무한대 값이 없는 경우 정수로 변환
    rounded_predicted_price = int(np.expm1(predicted_log_price[0]))

    response = make_response(f"예측된 가격: {rounded_predicted_price} 만원")
    return response

