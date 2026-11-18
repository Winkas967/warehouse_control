from functools import wraps
from flask import session, jsonify

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"message": "Não autenticado"}), 401
        return f(*args, **kwargs)
    return wrapper

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"message": "Não autenticado"}), 401
            
            if session.get("sector") not in roles:
                return jsonify({"message": "Acesso negado"}), 403
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"message": "Não autenticado"}), 401
        
        if (session.get("sector") or "").lower() != "admin":
            return jsonify({"message": "Acesso negado"}), 403
        
        return f(*args, **kwargs)
    return wrapper