from pydantic import BaseModel, validator
from pydantic.fields import ModelField

SHAPE_SINGLETON = 1
SHAPE_LIST = 2
SHAPE_SET = 3
SHAPE_MAPPING = 4
SHAPE_TUPLE = 5
SHAPE_TUPLE_ELLIPSIS = 6
SHAPE_SEQUENCE = 7
SHAPE_FROZENSET = 8
SHAPE_ITERABLE = 9
SHAPE_GENERIC = 10
SHAPE_DEQUE = 11
SHAPE_DICT = 12
SHAPE_DEFAULTDICT = 13
SHAPE_COUNTER = 14


class BaseSpecification(BaseModel):
    @validator('*', pre=True, always=True)
    def has_description(cls, v, field: ModelField):
        if field.field_info.description is None:
            if field.shape in (SHAPE_LIST, SHAPE_SET, SHAPE_MAPPING, SHAPE_TUPLE, SHAPE_DICT):
                raise ValueError(
                    f"Description missing for field {field.name} in Spec {cls.__name__}. Import Context from llama and use it to describe the field with natural language."
                )
            if field.type_ in (str, int, bool, float):
                raise ValueError(
                    f"Description missing for field {field.name} in Spec {cls.__name__}. Import Context from llama and use it to describe the field with natural language."
                )
        return v

    def _get_attribute_raw(self, name):
        return getattr(self, name)
