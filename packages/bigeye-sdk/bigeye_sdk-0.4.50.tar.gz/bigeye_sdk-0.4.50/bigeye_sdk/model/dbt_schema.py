from dataclasses import field
from typing import List, Optional

from pydantic import Field
from pydantic.dataclasses import dataclass
from pydantic_yaml import YamlModelMixin

from bigeye_sdk.model.protobuf_enum_facade import SimpleDbtTestToMetricType
from bigeye_sdk.serializable import YamlSerializable, PydanticSubtypeSerializable


class SimpleDbtColumn(PydanticSubtypeSerializable, type='column'):
    name: str = ""
    description: Optional[str] = None
    tests: Optional[List[SimpleDbtTestToMetricType]] = Field(default_factory=lambda: [])


class SimpleDbtModel(PydanticSubtypeSerializable, type='model'):
    name: str = ""
    description: Optional[str] = None
    columns: Optional[List[SimpleDbtColumn]] = Field(default_factory=lambda: [])


class SimpleDbtSchema(PydanticSubtypeSerializable, YamlSerializable):
    type = "schema"
    version: int = 0
    models: List[SimpleDbtModel] = Field(default_factory=lambda: [])
