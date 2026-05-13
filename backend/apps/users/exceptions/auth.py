class InvalidPasswordError(Exception):
    """Старий пароль невірний."""
    default_message= "Старий пароль невірний."

    def __init__(self, message: str=None):
        self.message=message or self.default_message
        super().__init__(self.message)


class InvalidTokenError(Exception):
    """Токен відновлення паролю невалідний або протермінований."""

    default_message = "Токен відновлення паролю невалідний або протермінований."

    def __init__(self,message: str = None):
        self.message = message or self.default_message
        super().__init__(self.message)
        