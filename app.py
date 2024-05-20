from dotenv import load_dotenv
load_dotenv()
 
from datetime import timedelta
import logging
import logging.config
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Lock
from file_process.process import processes
# from user_management.user_details import user_details
# from flask_jwt_extended import JWTManager
import secrets
 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
 
#Flask
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
 
# upload_folder_jd=cf.Resumes_File_Path+"\ResumeProcess\saved_jd_files"
# upload_folder_resume=cf.Resumes_File_Path+"\ResumeProcess\saved_resume_files"
# secret_key = secrets.token_urlsafe(16)
# app.config['JWT_SECRET_KEY'] = secret_key # Change this to a random secret key for your application
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
 
# jwt = JWTManager(app)
 
app.secret_key = "keepitsecret01"
 
# app.register_blueprint(user_details,url_prefix='/authenticate')
app.register_blueprint(processes,url_prefix='/mats/aura')
 
PREFIX = "/mats/aura"
@app.route(PREFIX + "/health", methods=['GET'])
def health_check():
   status = {
    "status": "OK_test"
    }
   logger.info(' test received GET request in health check endpoint')
   return jsonify(status), 200
 
 
mutex = Lock()
 
if __name__ == '__main__':
    app.run(debug=True,port =5000, host = '0.0.0.0')