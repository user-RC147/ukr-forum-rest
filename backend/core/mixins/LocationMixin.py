from django.db import models


class LocationMixin(models.Model):
    """
    Міксин локації без прямої залежності від geo моделей.
    Зберігає тільки id — не FK.
    """
    country_id=models.IntegerField(null=True,blank=True,verbose_name="ID країни")
    region_id=models.IntegerField(null=True,blank=True,verbose_name="ID регіону")
    city_id=models.IntegerField(null=True,blank=True,verbose_name="ID міста")


    class Meta:
        abstract=True

    


class PrivateLocationMixin(LocationMixin):
    """
    Локація з налаштуваннями приватності.
    """
    country_public=models.BooleanField(default=False)
    region_public=models.BooleanField(default=False)
    city_public=models.BooleanField(default=False)

    class Meta:
        abstract=True
        