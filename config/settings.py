import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import streamlit as st

# load_dotenv()

# class Settings(BaseSettings):
#     max_size_mb: int = Field(5, alias='MAX_CLIENT_UPLOAD_SIZE')
#     env:str = Field('DEV', alias='ENV')
#     prod_url:str = Field(None, alias='PROD_URL')
#     dev_url:str = Field(None, alias='DEV_URL')
    
#     @property
#     def backend_url(self) -> str:
#         if self.env == 'DEV':
#             return self.dev_url
#         elif self.env == 'PROD':
#             return self.prod_url
#         else:
#             return ''

#     @property
#     def max_size_bytes(self) -> int:
#         return self.max_size_mb * 1024 * 1024
    
#     model_config = SettingsConfigDict(env_file='.env', extra='ignore', populate_by_name=True)
class Settings:
    env: str = os.environ['ENV']
    max_size_mb:int = int(os.environ['MAX_CLIENT_UPLOAD_SIZE'])
    max_size_bytes:int = max_size_mb * 1024 * 1024
    backend_url:str = os.environ[str(env+'_URL')]

settings = Settings()