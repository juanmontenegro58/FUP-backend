from typing import (
    Tuple,
    Type, 
    TypeVar, 
    Generic, 
    List,
    Dict, 
    Any,
)
from django.db.models import (
    Model,
    QuerySet
)

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
    
    def filter(self, **kwargs) -> QuerySet[T]:
        return self.model.objects.filter(**kwargs)

    def delete(self, obj: T):
        obj.delete()

    def update(
        self, 
        obj_id: int | T, 
        data: Dict[str, Any]
    ) -> T:
        if isinstance(obj_id, self.model):
            obj = obj_id
        else:
            obj = self.get_by_id(obj_id = obj_id)

        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        obj.save()
        return obj
    
    def aggregate(
        self, 
        **kwargs
    ) -> Dict[str, Any]:
        return self.model.objects.aggregate(**kwargs)
    
    def get_or_create(self, item: Dict[str, Any]) -> Tuple[T, bool]:
        return self.model.objects.get_or_create(**item)