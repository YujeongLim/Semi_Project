import os

# os.environ["ORACLE_HOME"] = "/oraclexe/app/oracle/product/11.2.0/client_1"
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'oracle+cx_oracle://ADMIN:ADMIN@192.168.0.47:1521/XE') 
    
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    # SECRET_KEY = 'b3623a3c8a4943c6dd94a6bff0099d69'

    # connection = cx_Oracle.connect(user = "ADMIN", password="ADMIN",dsn="192.168.0.47:1521/REAL_ESTATE")