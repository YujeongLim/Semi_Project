# from app.quiz.app import app
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8086, debug=True)