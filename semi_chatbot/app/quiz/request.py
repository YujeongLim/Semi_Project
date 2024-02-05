# 클라이언트 요청 코드 예시
import requests
import json

url = 'https://d0da-58-72-151-124.ngrok-free.app/api/selectBeginner'

data = {
    "userRequest": {
        "timezone": "Asia/Seoul",
        "params": {
            "ignoreMe": "true"
        },
        "block": {
            "id": "465frphpaet64mlq25757a1x",
            "name": "블록 이름"
        },
        "utterance": "발화 내용",  # 실제 사용자의 발화 내용
        "lang": None,
        "user": {
            "id": "165053",  # 실제 사용자 ID
            "type": "accountId",
            "properties": {}
        }
    },
    "bot": {
        "id": "65a5ecae7508a77e89354145",
        "name": "봇 이름"
    },
    "action": {
        "name": "o81t489qhq",
        "clientExtra": None,
        "params": {
            "utterance": "answer"
        },
        "id": "io90hv7djgbqld34b4ee3xbp",
        "detailParams": {
            "utterance": {
                "origin": "answer",
                "value": "answer",
                "groupName": ""
            }
        },
        "user_state": {
        "user_id": "165053"
        }
    }
}

headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.status_code)
print(response.json())
