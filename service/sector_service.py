from model.sector_model import Sector, SectorModel

class SectorService:
    @staticmethod
    def get_all():
        try:
            sector = SectorModel.get_all()
            
            return sector
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_name(name):
        try:
            if not name:
                raise ValueError("Nenhum nome foi passado")
            
            sector = SectorModel.get_by_name(name)
            
            return sector
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_id(id):
        try:
            if not id:
                raise ValueError("Nenhum ID foi passado")
            
            sector = SectorModel.get_by_id(id)
            
            return sector
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def create(data):
        try:
            if not data:
                raise ValueError("Nenhum dado foi passado")
            
            name = (data.get('name') or '').strip()
            description = data.get('description') or ''
            
            sector = SectorModel.create(name, description)
            
            return sector
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def delete(id):
        try:
            if not id:
                raise ValueError("Nenhum ID foi passado")
            
            sector = SectorModel.delete(id)
            
            return sector
        except Exception as e:
            raise Exception(str(e))