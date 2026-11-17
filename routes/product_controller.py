from flask import Blueprint, jsonify, request
from service.product_service import ProductService

product_route = Blueprint('product_route', __name__)

@product_route.route("/product", methods=['GET'])
def get_all():
    try:
        
        products = ProductService.get_all()
        
        return jsonify([
            product.to_dict()
            for product in products
        ])
        
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@product_route.route("/product/<string:name>", methods=['GET'])
def get_by_name(name):
    try:
        
        products = ProductService.get_by_name(name)
        
        if not products:
            return jsonify({
                "message": "Nenhum produto encontrado com esse nome"
            }), 404
            
        return jsonify(products.to_dict())
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@product_route.route("/product/<int:id>", methods = ['GET'])
def get_by_id(id):
    try:
        
        products = ProductService.get_by_id(id)
        
        if not products:
            return jsonify({
                "message": "Nenhum produto encontrado com esse id"
            }), 404
            
        return jsonify(products.to_dict())
    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500
        
@product_route.route("/product", methods = ["POST"])
def create():
    try:
        data = request.get_json()
        
        create_product = ProductService.create(data)

        return jsonify(create_product.to_dict())
    except Exception as e:
        raise Exception(str(e))
    
@product_route.route("/delete/product/<int:id>", methods = ["POST"])
def delete(id):
    try:
        
        delete_product = ProductService.delete(id)
        
        return jsonify(delete_product)
    except Exception as e:
        raise Exception(str(e))
    
@product_route.route("/update/product/<int:id>", methods = ["POST"])
def update(id):
    try:
        
        data = request.get_json()
        
        update_product = ProductService.update(id, data)
        
        return jsonify(update_product.to_dict())
    except Exception as e:
        raise Exception(str(e))
    
    