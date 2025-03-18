from typing import Type, TypeVar, Generic, List
from django.db.models import Model

T = TypeVar("T", bound=Model)

class RepositoryInterface(Generic[T]):
    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def get_by_id(self, obj_id: int) -> T:
        return self.model.objects.get(id=obj_id)

    def list_all(self) -> List[T]:
        return self.model.objects.all()

    def delete(self, obj: T):
        obj.delete()
