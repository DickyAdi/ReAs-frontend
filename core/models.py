from pydantic import BaseModel, Field, HttpUrl, model_validator
from typing import Literal, Optional
import uuid
import requests
from requests import Response
from urllib.parse import urljoin

from typing_extensions import Self, TypedDict

from config.settings import settings

class Topics(TypedDict):
    trend_topics:list[dict]
    frequent_topics:list[dict]
    count:int

class ResponseData(TypedDict):
    positive:Topics
    negative:Topics
    number_valid_rows:int

class RequestModel(BaseModel):
    uid:str = Field(default_factory=lambda : uuid.uuid4().hex)
    backend_url_path:HttpUrl = Field(settings.backend_url)
    endpoint:str
    method:Literal['post', 'get']
    params:dict = Field(default_factory=dict)
    @property
    def full_url(self):
        return urljoin(self.backend_url_path, self.endpoint)
    
    @model_validator(mode='after')
    def fix_endpoint(self) -> Self:
        if not self.endpoint.startswith('/'):
            self.endpoint = '/' + self.endpoint
        return self

    def send_request(self, files:Optional[dict]=None) -> Response:
        full_params = {'id' : self.uid, **self.params}
        if self.method == 'post':
            response = requests.post(self.full_url, files=files, params=full_params)
            return response
        elif self.method == 'get':
            response = requests.get(self.full_url, params=full_params)
            return response
        else:
            raise NotImplementedError(f'{self.method} method not implemented.')

class ExtractionResponse(BaseModel):
    status:str
    code:int
    message:str
    error:Optional[str] = None
    data:Optional[ResponseData] = None