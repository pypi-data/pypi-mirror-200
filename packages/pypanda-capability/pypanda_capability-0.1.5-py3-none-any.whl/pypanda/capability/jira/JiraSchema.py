import datetime
from typing import List, Optional, Union

from pydantic import BaseModel


class FreeFieldsSchema(BaseModel):
    fieldId: str
    label: str
    value: Optional[Union[str, dict, list]]


class ServiceDeskRequestSchema(BaseModel):
    serviceDeskId: int
    requestTypeId: int
    requestTypeName: Optional[str]
    requestFieldValues: Optional[List[FreeFieldsSchema]]


class IssueTypeSchema(BaseModel):
    self: str
    id: int
    description: str
    name: str
    iconUrl: str
    subtask: bool
    avatarId: int


class IssueSchema(BaseModel):
    issueKey: str
    labels: List[str]
    status: str
    summary: Optional[str]
    created: datetime.datetime
    reporter: Optional[str]
    assignee: Optional[str]
    project: str
    request: Optional[ServiceDeskRequestSchema]
    forms: Optional[List[dict]]
    issueType: IssueTypeSchema
    updated: datetime.datetime

    class Config:
        arbitrary_types_allowed = True
