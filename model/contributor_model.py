from database.connection import get_db_connection

class Contributor:
    def __init__(self, name, id=None, id_sector=None):
        self.id = id
        self.name = name
        self.id_sector = id_sector
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "id_sector": self.id_sector
        }
        
class ContributorModel:
    @staticmethod
    def get_all():
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT id, id_sector, name
                FROM contributor
            """
            
            cursor.execute(sql)
            
            contributorData = cursor.fetchall()
            
            if not contributorData:
                return []
            
            contributor = [
                Contributor(**contributor)
                for contributor in contributorData
            ]
            
            return contributor
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
                SELECT id, id_sector, name
                FROM contributor
                WHERE id = %s
            """
            cursor.execute(sql, (id,))
            
            contributorData = cursor.fetchone()
            
            if not contributorData:
                return None
            
            contributor = Contributor(**contributorData)
            
            return contributor
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
                SELECT id, id_sector, name
                FROM contributor
                WHERE name = %s
            """
            
            cursor.execute(sql, (name,))
            
            contributorData = cursor.fetchone()
            
            if not contributorData:
                return None
            
            contributor = Contributor(**contributorData)
            
            return contributor
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
                
    @staticmethod
    def create(name, id_sector):
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                INSERT INTO contributor(name, id_sector)
                VALUES (%s, %s)
                RETURNING id, name, id_sector
            """
            
            cursor.execute(sql, (name, id_sector,))
            
            contributorCreate = cursor.fetchone()
            
            conn.commit()
            
            contributor = Contributor(**contributorCreate)
            
            return contributor
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
                DELETE FROM contributor
                WHERE id = %s
            """
            
            cursor.execute(sql, (id,))
            conn.commit()
            
            return True
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()

    @staticmethod
    def get_all_for_selection():
        conn = None
        cursor = None
        
        try:
            conn, cursor = get_db_connection()
            
            sql = """
                SELECT c.id, c.id_sector, c.name
                FROM contributor c
                INNER JOIN sector s ON s.id = c.id_sector
                WHERE LOWER(TRIM(s.name)) <> 'admin'
                ORDER BY c.name
            """
            
            cursor.execute(sql)
            data = cursor.fetchall()
            
            return [
                Contributor(**contributor)
                for contributor in data
            ]
            
        except Exception as e:
            raise Exception(str(e))
        finally:
            if conn:
                conn.close()
            if cursor:
                cursor.close()
            