from model.contributor_model import Contributor, ContributorModel

class ContributorService:
    @staticmethod
    def get_all():
        try:
            
            contributor = ContributorModel.get_all() 
       
            return contributor
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_name(name):
        try:
            if not name:
                raise ValueError("Nenhum nome passado")
            
            contributor = ContributorModel.get_by_name(name)
            
            return contributor
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_id(id):
        try:
            
            if not id:
                raise ValueError("Nenhum ID passado")
            
            contributor = ContributorModel.get_by_id(id)
            
            return contributor
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def create(data):
        try:
            if not data:
                raise ValueError("Nenhum dado passado")
            
            name = (data.get('name') or "").strip()
            id_sector = data.get('id_sector') or ""
            
            contributorCreate = ContributorModel.create(name, id_sector)
            
            return contributorCreate
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def delete(id):
        try:
            if not id:
                raise ValueError("Nenhum ID passado")
            
            contributorDelete = ContributorModel.delete(id)
            
            return contributorDelete
        except Exception as e:
            raise Exception(str(e))
            
        