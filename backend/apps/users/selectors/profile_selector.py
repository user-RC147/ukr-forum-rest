from apps.users.models import CustomUser

def get_profile(user:CustomUser)->CustomUser:
    """
    Повертає профіль користувача.
    В майбутньому тут може бути:
    - перевірка чи не заблокований акаунт
    - підрахунок статистики
    - кешування
    """
    return user