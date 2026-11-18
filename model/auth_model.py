from database.connection import get_db_connection

class Auth:
    def __init__(self, name, password, id=None, id_sector=None, sector=None):
        self.name = name
        self.password = password
        self.id = id
        self.id_sector = id_sector
        self.sector = sector
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_sector": self.id_sector,
            "sector": self.sector
        }
    
class AuthModel:
    @staticmethod
    def login(name, password):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT c.id, c.name, c.password, c.id_sector, s.name AS sector
                FROM contributor c
                LEFT JOIN sector s ON s.id = c.id_sector
                WHERE c.name = %s AND c.password = %s
            """
            cursor.execute(sql, (name, password,))

            loginData = cursor.fetchone()
            
            if not loginData:
                raise ValueError("Nome ou senha incorretos")
            
            login = Auth(**loginData)
            
            return login
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
    