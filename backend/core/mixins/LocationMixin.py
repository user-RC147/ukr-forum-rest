from django.db import models


class LocationMixin(models.Model):
    """
    Абстрактний клас для локації.
    Підключається до будь-якої моделі через наслідування.
    
    Приклад використання:
        class CustomUser(AbstractUser, LocationMixin):
            ...
        
        class Advertisement(models.Model, LocationMixin):
            ...
    """

    country=models.ForeignKey(
        'geo.Country',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Країна',
        related_name="%(app_label)s_%(class)s_country" # Створює унікальне ім'я для кожної моделі
    )
    region=models.ForeignKey(
        'geo.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Регіон',
        related_name="%(app_label)s_%(class)s_region",

    )
    city=models.ForeignKey(
        'geo.City',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Місто",
        related_name="%(app_label)s_%(class)s_city",
    )

    def get_location_display(self):
        """Повна локація."""
        parts=[]
        if self.country:
            parts.append(f"{self.country.flag_emoji} {self.country.name}")
        if self.region:
            parts.append(f"{self.region.name}")
        if self.city:
            parts.append(f"{self.city.name}")
        return",".join(parts) if parts else None
    
    class Meta:
        abstract=True


class PrivateLocationMixin(LocationMixin):
    """
    Для користувача — локація з налаштуваннями приватності.
    """
    country_public=models.BooleanField(
        default=False,
        verbose_name="Країна публічна"
    )
    region_public=models.BooleanField(
        default=False,
        verbose_name="Регіон публічний"
    )
    city_public=models.BooleanField(
        default=False,
        verbose_name="Міто публічне"
    )

    def get_location_display(self,public_only=False):
        """
        public_only=False → повна локація (для власника)
        public_only=True  → тільки публічні поля (для інших)
        """
        parts=[]
        if self.country:
            if not public_only or self.country_public:
                parts.append(f"{self.country.flag_emoji} {self.country.name}")
        if self.region:
            if not public_only or self.region_public:
                parts.append(f"{self.region.name}")
        if self.city:
            if not public_only or self.city_public:
                parts.append(f"{self.city.name}")
        return ", ".join(parts) if parts else None
    
    class Meta:
        abstract=True
            