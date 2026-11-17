from flask import Blueprint, jsonify, request
from service.contributor_service import ContributorService

contributor_route = Blueprint('contributor_route', __name__)

@contributor_route.route("/contributor", methods=['GET'])
def get_all():
    try:
        
        contributorAll = ContributorService.get_all()
        
        return jsonify([
            contributor.to_dict()
            for contributor in contributorAll
        ])
        
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500

@contributor_route.route("/contributor/<string:name>", methods=['GET'])        
def get_by_name(name):
    try:
        
        contributorName = ContributorService.get_by_name(name)
        
        if not contributorName:
            return jsonify({
                "message": "Nenhum nome encontrado"
            }), 500
        
        return jsonify(contributorName.to_dict())
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@contributor_route.route("/contributor/<int:id>", methods=['GET'])
def get_by_id(id):
    try:
        
        contributorID = ContributorService.get_by_id(id)
        
        if not contributorID:
            return jsonify({
                "message": "Nenhum ID encontrado"
            })
        return jsonify(contributorID.to_dict())
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@contributor_route.route("/contributor", methods=['POST'])
def create():
    try:
        
        data = request.get_json()
        
        contributorCreate = ContributorService.create(data)
        
        return jsonify(contributorCreate.to_dict())
    except Exception as e:
        raise Exception(str(e))
        
        
@contributor_route.route("/contributor/delete/<int:id>", methods=['DELETE'])
def delete(id):
    try:
        
        contributorDelete = ContributorService.delete(id)
        
        return jsonify(contributorDelete)
    except Exception as e:
        raise Exception(str(e))
        