import logging
from flask import request, jsonify, Blueprint
import utils.config as cf
from flask_cors import CORS
from utils.pencrypt import encrypt, decrypt
from flask_jwt_extended import get_jwt, create_access_token, decode_token
from utils import jwt_validation


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('users.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

user_details = Blueprint("user_details", __name__)

@user_details.route('/login', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']
            if username == 'matsdev@mouritech.org' or username == 'shailendrat.in@mouritech.com':
                access_token = create_access_token(identity=username)
                logger.info(f"User '{username}' logged in successfully")
                return jsonify({"msg": "Login Successful", "access_token": access_token})
            else:
                logger.error(f"Failed login attempt with username: '{username}'")
                return jsonify({"error": "The username is incorrect"})
        except Exception as e:
            logger.error(f"Error occurred during login: {str(e)}")
            return jsonify({"error": "Something went wrong while logging in"})

@user_details.route('/validate-token', methods=['POST'])
def validate_token():
    token = request.json.get('access_token')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        decoded_token = decode_token(token)
        logger.info(f"Token validated for user: {decoded_token['sub']}")
        return jsonify({'message': 'Token is valid', 'user': decoded_token['sub']}), 200
    except Exception as e:
        logger.error(f"Error occurred during token validation: {str(e)}")
        return jsonify({'message': 'Invalid token', 'error': str(e)}), 401
