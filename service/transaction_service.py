from model.transaction_model import TransactionModel

class TransactionService:
    @staticmethod
    def get_all():
        try:
            
            transactionData = TransactionModel.get_all()
            
            return transactionData
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def get_by_id(id):
        try:
            
            if not id:
                raise ValueError("Nenhum ID foi passado")
            
            transactionData = TransactionModel.get_by_id(id)
            
            return transactionData
        except Exception as e:
            raise Exception(str(e))
        
    @staticmethod
    def create(data):
        try:
            
            if not data:
                raise ValueError("Nenhum dado foi passado")
            
            id_product = data.get('id_product')
            id_contributor = data.get('id_contributor')
            date_transaction = data.get('date_transaction')
            amount = data.get('amount')
            type = data.get('type')
            
            if id_product is None:
                raise ValueError("Produto obrigatório")
            if id_contributor is None:
                raise ValueError("Colaborador obrigatório")
            if not date_transaction:
                raise ValueError("Data obrigatória")
            if not isinstance(amount, int) or isinstance(amount, bool) or amount <= 0:
                raise ValueError("Quantidade deve ser um inteiro maior que zero")
            if type not in ("entrada", "saida"):
                raise ValueError("Tipo deve ser 'entrada' ou 'saida'")
            
            transactionData = TransactionModel.create(id_product, id_contributor, date_transaction, amount, type)
            
            return transactionData
        except Exception as e:
            raise Exception(str(e))