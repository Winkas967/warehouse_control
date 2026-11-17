from database.connection import get_db_connection

class Product:
    def __init__(self, name, description, amount, id=None):
        self.id = id
        self.name = name
        self.description = description
        self.amount = amount
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "amount": self.amount
        }
        
class ProductModel:
    @staticmethod
    def get_all():
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT id, name, description, amount
                FROM product
            """
            
            cursor.execute(sql)
            
            productData = cursor.fetchall()
            
            if not productData:
                return None
            
            products = [
                Product(**product)
                for product in productData
            ]
            
            return products
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
                
    @staticmethod
    def get_by_name(name):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT id, name, description, amount
                FROM product
                WHERE name = %s
            """
            
            cursor.execute(sql, (name,))
            productData = cursor.fetchone()
            
            if not productData:
                return None
            
            product = Product(**productData)
            
            return product
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
    @staticmethod
    def get_by_id(id):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT id, name, description, amount
                FROM product
                WHERE id = %s
            """
            
            cursor.execute(sql, (id,))
            producData = cursor.fetchone()
            
            if not producData:
                return None
            
            product = Product(**producData)
            
            return product
        except Exception as e:
            raise Exception(str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    @staticmethod
    def create(name, description, amount):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                INSERT INTO product (name, description, amount)
                VALUES(%s, %s, %s)
                RETURNING id, name, description, amount
            """
            cursor.execute(sql, (name, description, amount),)
            
            productCreate = cursor.fetchone()
            
            conn.commit()
            
            product = Product(**productCreate)
            
            return product
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
            
                
    @staticmethod
    def update(id, name, description, amount):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                UPDATE product
                SET name = %s, description = %s, amount = %s
                WHERE id = %s
                RETURNING id, name, description, amount
            """
            
            cursor.execute(sql, (name, description, amount, id))
            productUpdate = cursor.fetchone()
            conn.commit()
            
            product = Product(**productUpdate)
            
            return product
        except Exception as e:
            raise Exception(str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()    
        
    @staticmethod
    def delete(id):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                DELETE FROM product
                WHERE id = %s
            """
            
            cursor.execute(sql, (id,))
            conn.commit()
            
            return True 
        except Exception as e:
            raise Exception(str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
        
            