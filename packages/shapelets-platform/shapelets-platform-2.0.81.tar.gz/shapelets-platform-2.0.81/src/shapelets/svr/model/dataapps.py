from pydantic import BaseModel
from typing import Optional, Set
from typing_extensions import Literal

DataAppField = Literal['name', 'major', 'minor', 'description', 'creationDate', 'updateDate', 'specId', 'tags']
DataAppAllFields: Set[DataAppField] = set(
    ['name', 'major', 'minor', 'description', 'creationDate', 'updateDate', 'specId', 'tags'])


class DataAppProfile(BaseModel):
    name: str
    major: Optional[int]
    minor: Optional[int]
    description: Optional[str] = None
    creationDate: Optional[int] = None
    updateDate: Optional[int] = None
    specId: Optional[str] = None
    tags: Optional[list] = None
