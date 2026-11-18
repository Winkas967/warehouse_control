from flask import Blueprint, request, jsonify, session
from service.auth_service import AuthService

auth_route = Blueprint("auth_route", __name__)

@auth_route.route("/login", methods=['POST'])
def login():
    try:
        
        data = request.get_json()
        
        loginData = AuthService.login(data)
        
        session["user_id"] = loginData.id
        session["sector"] = loginData.sector
        
        return jsonify(loginData.to_dict()), 200
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 401

@auth_route.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "ok"}), 200
