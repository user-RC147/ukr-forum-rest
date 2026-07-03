


class ProductNotFoundException:
    def __init__(self,message='ProductNotFound'):
        self.message=message
        super().__init__(self.message)
    
    
class  ProductAlreadyExistsException(Exception):

    def __init__(self,message='ProductAlreadyExists'):
        self.message=message
        super().__init__(self.message)  
