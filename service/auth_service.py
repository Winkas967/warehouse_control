from model.auth_model import AuthModel

class AuthService:
    @staticmethod
    def login(data):
        try:
            if not data:
                raise ValueError("Nenhum dado foi passado")
            
            name = data.get('name')
            password = data.get('password')
            
            loginData = AuthModel.login(name, password)
            
            return loginData
        except Exception as e:
            raise Exception(str(e))