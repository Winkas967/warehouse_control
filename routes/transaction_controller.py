from flask import Blueprint, request, jsonify
from service.transaction_service import TransactionService

transaction_route = Blueprint('transaction_route', __name__)

@transaction_route.route("/transaction", methods=['GET'])
def get_all():
    try:
        transactionData = TransactionService.get_all()
        
        return jsonify([
            transaction.to_dict()
            for transaction in transactionData
        ])
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@transaction_route.route("/transaction/<int:id>", methods=['GET'])
def get_by_id(id):
    try:
        
        transactionData = TransactionService.get_by_id(id)
        
        return jsonify(transactionData.to_dict())
    except Exception as e:
        return jsonify({
            "message", str(e)
        }), 500
        
@transaction_route.route("/transaction/create", methods=['POST'])
def create():
    try:
        
        data = request.get_json()
        
        transactionData = TransactionService.create(data)
        
        return jsonify(transactionData.to_dict())
    except Exception as e:
        raise Exception(str(e))