from model.product_model import ProductModel, Product

class ProductService():
    @staticmethod
    def get_all():
        try:
            products = ProductModel.get_all()
            
            return products
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_name(name):
        try:
            if not name:
                raise ValueError("Nenhum nome foi selecionado")
            
            productName = ProductModel.get_by_name(name)
            
            return productName
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_id(id):
        try:
            
            if not id:
                raise ValueError("Nenhum id foi selecionado")
            
            productId = ProductModel.get_by_id(id)
            
            return productId
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def create(data):
        try:
            
            if not data:
                raise ValueError("Nenhum dado foi recebio")
            
            name = (data.get('name') or '').strip()
            description = data.get('description') or ''
            amount = data.get('amount') or ''
            
            if not name:
                raise ValueError("Nenhum nome foi passado")
                        
            if not amount:
                raise ValueError("Nenhum valor foi passado")
            
            productCreate = ProductModel.create(name, description, amount)
            
            return productCreate
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def update(id, data):
        try:
            
            if not id:
                raise ValueError("Nenhum id foi selecionado")
            
            name = (data.get('name') or '').strip()
            description = data.get('description') or ''
            amount = data.get('amount')
            
            if not name:
                raise ValueError("Nenhum nome foi selecionado")

            productUpdate = ProductModel.update(id, name, description, amount)
            
            return productUpdate
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def delete(id):
        try:
            
            if not id:
                raise ValueError("Nenhum id foi selecionado")
            
            productDelete = ProductModel.delete(id)
            
            return productDelete
        except Exception as e:
            raise Exception(str(e))
        
        
        