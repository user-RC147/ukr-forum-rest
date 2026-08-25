from apps.geo.contracts.country_contract import get_country_contract
from apps.geo.contracts.region_contract import get_region_contract
from apps.geo.contracts.city_contract import get_city_contract


from apps.users.selectors.star_selector import StarSelector
from apps.users.dto.user_dto import UserStarOutDTO
from apps.users.dto._to_dto_location import _to_dto_out_location,_get_ids_location,_get_locations

from core.func_print import prt

class StarService:

    def __init__(self):
        self._selector = StarSelector()
    
    
    def get_all_user(self):
        users = self._selector.get_all_user_grouped()

        ids = _get_ids_location(users)
        location = _get_locations(ids,get_country_contract(), get_region_contract(), get_city_contract())

        
        dtos=[UserStarOutDTO(
            id=user.id,
            location=_to_dto_out_location(user.location,location)
        )for user in users]

      
        return dtos