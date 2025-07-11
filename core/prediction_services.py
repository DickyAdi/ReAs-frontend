from pydantic import BaseModel, Field, HttpUrl
from typing import Literal
import uuid
import requests
from urllib.parse import urljoin

from config.settings import settings

class RequestModel(BaseModel):
    uid:str = Field(default_factory=lambda : uuid.uuid4().hex)
    backend_url_path:HttpUrl = settings.backend_url
    def __init__(self, endpoint:str, files=None, param:dict=None):
        self.endpoint:str = Field(...)
        self.files = Field(None)
        self.params = Field(None)
    def get_api(self):
        return urljoin(self.backend_url_path, self.endpoint)
    def send_request(self, method:Literal['post', 'get']):
        if method == 'post':
            requests.post(self.get_api(), files=self.files, params=self.params)