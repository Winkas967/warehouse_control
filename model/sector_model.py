from database.connection import get_db_connection

class Sector:
    def __init__(self, name, description, id=None):
        self.name = name
        self.description = description
        self.id = id
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
        
class SectorModel:
    @staticmethod
    def get_all():
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
               SELECT id, name, description
               FROM sector 
            """
            cursor.execute(sql)
            
            sectorData = cursor.fetchall()
            
            if not sectorData:
                return None
            
            sector = [
                Sector(**sector)
                for sector in sectorData
            ]
            
            return sector
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
                SELECT id, name, description
                FROM sector
                WHERE id = %s
            """
            cursor.execute(sql, (id,))
            
            sectorData = cursor.fetchone()
            
            if not sectorData:
                return None
            
            sector = Sector(**sectorData)

            
            return sector
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
                SELECT id, name, description
                FROM sector
                WHERE name = %s
            """
            cursor.execute(sql, (name,))
            
            sectorData = cursor.fetchone()
            
            if not sectorData:
                return None
            
            sector = Sector(**sectorData)
            
            return sector
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
    @staticmethod
    def create(name, description):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                INSERT INTO sector(name, description)
                VALUES(%s, %s)
                RETURNING id, name, description
            """
            
            cursor.execute(sql, (name, description))
            
            sectorData = cursor.fetchone()
            
            conn.commit()
            
            if not sectorData:
                return None
            
            sector = Sector(**sectorData)
                
            return sector
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
    @staticmethod
    def delete(id):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                DELETE FROM sector
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
            