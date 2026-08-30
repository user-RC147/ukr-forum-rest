from config.exceptions import NotFoundError


class UserNotFoundException(NotFoundError):

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.default_message = "user not found"
        self.default_code = "not_found"
        super().__init__(f"User with id {user_id} not found.")

    
