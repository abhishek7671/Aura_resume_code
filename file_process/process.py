import logging
from flask import request, jsonify, Blueprint
import utils.config as cf
import base64
from file_process.Resume_Scoring import get_skill_process,bg_process
# from utils import jwt_validation
 


processes = Blueprint("processes", __name__)

# Configuring logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('process.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

upload_folder_jd = cf.Resumes_File_Path + "\ResumeProcess\saved_jd_files"
upload_folder_resume = cf.Resumes_File_Path + "\ResumeProcess\saved_resume_files"





@processes.route("/view_data", methods=['POST'])
# @jwt_validation.is_jwt_valid()
def upload_and_view_data():
    try:
        if request.method == 'POST':
            resume_file = request.files['resume']
            if resume_file:
                resume_content = resume_file.read()
                base64_resume = base64.b64encode(resume_content).decode('utf-8')
               
                request_data = {
                    "resume_folder": [resume_file.filename],
                    "resfile": [base64_resume]
                }
               
                # Log a debug message
                logger.debug("Received a request to upload and view data.")
               
                return get_skill_process(request_data)
    except Exception as e:
        # Log the error
        logger.error(f"Error occurred during data upload and processing: {str(e)}")
        return jsonify({
            "Status": "Something went wrong while processing the request",
            "Error": str(e),
            "Error_code": 1
        })














@processes.route("/view_result", methods=['POST'])
# @jwt_validation.is_jwt_valid()
def process_resume():
    try:
        if request.method == 'POST':
            resume_file = request.files['resume']
            if resume_file:
                resume_content = resume_file.read()
                base64_resume = base64.b64encode(resume_content).decode('utf-8')
               
                mandatory_skills = request.form.getlist('mandatory_skills')
                secondary_skills = request.form.getlist('secondary_skills')
                experience = request.form.get('experience')
                job_input = request.form.get('job_input')
                jd_input = request.form.get('jd_input')
               
                request_data = {
                    "resume_folder": [resume_file.filename],
                    "resfile": [base64_resume],
                    "mandatory_skills": mandatory_skills,
                    "secondary_skills": secondary_skills,
                    "experience": experience,
                    "job_input":job_input,
                    "jd_input":jd_input
                }
               
                # Log a debug message
                logger.debug("Received a request to process resume.")
               
                response_data = bg_process(request_data)
               
                return jsonify(response_data)
    except Exception as e:
        # Log the error
        logger.error(f"Error occurred during resume processing: {str(e)}")
        return jsonify({
            "Status": "Something went wrong while processing the request",
            "Error": str(e),
            "Error_code": 1
        })
