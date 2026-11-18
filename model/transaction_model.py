from database.connection import get_db_connection

class Transaction:
    def __init__(self, date_transaction, amount, type, id_product=None, id_contributor=None, id=None):
        self.date_transaction = date_transaction
        self.amount = amount
        self.type = type
        self.id_product = id_product
        self.id_contributor = id_contributor
        self.id = id
        
    def to_dict(self):
        return {
            "id": self.id,
            "id_product": self.id_product,
            "id_contributor": self.id_contributor,
            "date_transaction": self.date_transaction,
            "amount": self.amount,
            "type": self.type
        }
        
class TransactionModel:
    @staticmethod
    def get_all():
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT id, id_product, id_contributor, date_transaction, amount, type
                FROM transaction
            """
            
            cursor.execute(sql)
            
            transactionData = cursor.fetchall()
            
            if not transactionData:
                return []
            
            transaction = [
                Transaction(**transaction)
                for transaction in transactionData
            ]
            
            return transaction
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
                SELECT id, id_product, id_contributor, date_transaction, amount, type
                FROM transaction
                WHERE id = %s
            """
            
            cursor.execute(sql,(id,))
            
            transactionData = cursor.fetchone()
            
            if not transactionData:
                return None
            
            transaction = Transaction(**transactionData)
            
            return transaction
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
    @staticmethod
    def create(id_product, id_contributor, date_transaction, amount, type):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()

            delta = amount if type == "entrada" else -amount
            
            sql = """
                UPDATE product
                SET amount = amount + %s
                WHERE id = %s AND amount + %s >= 0
            """
            cursor.execute(sql, (delta, id_product, delta),)
            
            if cursor.rowcount == 0:
                raise ValueError("Produto não encontrado ou estoque insuficiente")
            
            sql2 = """
                INSERT INTO transaction (id_product, id_contributor, date_transaction, amount, type)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, id_product, id_contributor, date_transaction, amount, type
            """
            
            cursor.execute(sql2, (id_product, id_contributor, date_transaction, amount, type))
            
            row = cursor.fetchone()
            
            conn.commit()
            return Transaction(**row)
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()

            
            
            
            
            
            