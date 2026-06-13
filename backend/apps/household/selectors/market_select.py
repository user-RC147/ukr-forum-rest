from typing import Optional
from django.db.models import Q

from apps.household.models.market import Market



class MarketSelector:
    """
    Селектор відповідає ТІЛЬКИ за вибірку даних, пошук та сортування (Запити).
    """

    def get_market_list(self, 
                        search_query:str=None,
                        country_id:int=None,
                        region_id:int=None,
                        city_id:int=None,
                        ordering:str='name'
                        )->list[Market]:
        """
        Повертає відфільтрований та відсортований список магазинів.
        """
        # Починаємо з базового QuerySet
        queryset=Market.objects.all()
        
        # 1. Гнучка фільтрація за гео-локацією
        if country_id:
            queryset=queryset.filter(country_id=country_id)
        if region_id:
            queryset=queryset.filter(region_id=region_id)
        if city_id:
            queryset=queryset.filter(city_id=city_id)

        # 2. Текстовий пошук (за назвою або адресою)
        if search_query:
            queryset=queryset.filter(
                Q(name__icontains=search_query)|Q(address_line__icontains=search_query)
            )
        
        # 3. Сортування (наприклад, за алфавітом "name" або новіші "-id")
        allwed_arderings=['name','-name','id','-id']
        if ordering in allwed_arderings:
            queryset = queryset.order_by(ordering)
        else:
            queryset=queryset.order_by('name') # дефолтне сортування

        return list(queryset)


    def get_market_by_id(self,market_id:int)->Optional[Market]:
        """Деталка одного магазину"""
        return Market.objects.filter(id=market_id).first()