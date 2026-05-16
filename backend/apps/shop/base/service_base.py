# shared/services/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type
from django.core.exceptions import ObjectDoesNotExist
import logging
from apps.shop.exceptions import ProductNotFound

logger = logging.getLogger("shop")

T = TypeVar("T")

class AbstractService(ABC, Generic[T]):

    @abstractmethod
    def get(self, id: int) -> T:
        ...

    @abstractmethod
    def create(self, data: dict) -> T:
        ...

    @abstractmethod
    def update(self, id: int, data: dict) -> T:
        ...

    @abstractmethod
    def delete(self, id: int) -> None:
        ...

class BaseService(AbstractService[T]):
    def __init__(self, model: Type[T]):
        super().__init__()
        self.model = model
    

    def get(self, id: int) -> T:
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            logger.info("%s not found: pk=%s", self.model.__name__, id)
            raise ProductNotFound(f"id:{id} from model:{self.model.__name__} not found")


    def create(self, data: dict) -> T:
        return self.model.objects.create(**data)

    def update(self, id: int, data: dict) -> T:
        self.get(id)

        self.model.objects.filter(id=id).update(**data)
        return self.model.objects.get(id=id)
    

    def delete(self, id: int) -> None:
        self.get(id)
        self.model.objects.get(id=id).delete()