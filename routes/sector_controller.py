from flask import Blueprint, jsonify, request
from service.sector_service import SectorService

sector_route = Blueprint('sector_route', __name__)

@sector_route.route("/sector", methods=['GET'])
def get_all():
    try:
            
        sectors = SectorService.get_all()

        return jsonify([
            sector.to_dict()
            for sector in sectors
        ])
        
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@sector_route.route("/sector/<int:id>", methods=['GET'])
def get_by_id(id):
    try:
        
        sectors = SectorService.get_by_id(id)
        
        return jsonify(sectors.to_dict())
          
    
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@sector_route.route("/sector/<string:name>", methods=['GET'])
def get_by_name(name):
    try:
        
        sectors = SectorService.get_by_name(name)
        
        return jsonify(sectors.to_dict())
            
        
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@sector_route.route("/sector/create", methods=['POST'])
def create():
    try:
        
        data = request.get_json()
        
        sectors = SectorService.create(data)
        
        return jsonify(sectors.to_dict())
    except Exception as e:
        raise Exception(str(e))
    
@sector_route.route("/sector/delete/<int:id>", methods=['DELETE'])
def delete(id):
    try:
        
        sectors = SectorService.delete(id)
        
        return jsonify(sectors)
    except Exception as e:
        raise Exception(str(e))
