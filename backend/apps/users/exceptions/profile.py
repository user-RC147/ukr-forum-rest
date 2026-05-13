class ProfileUpdateError(Exception):
    """Помилка оновлення профілю."""
    default_message = "Помилка оновлення профілю."

    def __init__(self,message: str=None):
        self.message = message or self.default_message
        super().__init__(self.message)

