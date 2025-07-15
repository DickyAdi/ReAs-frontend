from io import BytesIO
import requests
import pandas as pd
from millify import millify

from typing import Any, Annotated, Optional

from .models import RequestModel, ExtractionResponse

def submit_extract_request(files:dict, text_column:str, endpoint:Optional[str]='extract') -> ExtractionResponse:
    try:
        params = {'text_column': text_column}
        response = RequestModel(endpoint=endpoint, method='post', params=params).send_request(files)
        response.raise_for_status()
        data = response.json()
        return ExtractionResponse(
            status=data.get('status'),
            code=data.get('code'),
            message=data.get('message'),
            data=data.get('data')
        )
    except requests.exceptions.HTTPError as e:
        return ExtractionResponse(
            status='error',
            code=e.response.status_code,
            error='HTTPError',
            message=e.response.reason
        )
    except requests.exceptions.ConnectTimeout:
        return ExtractionResponse(
            status='error',
            code=408,
            error='ConnectionTimeout',
            message='Request timeout while connecting to the server.'
        )

    except requests.exceptions.ConnectionError:
        return ExtractionResponse(
            status='error',
            code=503,
            error='ConnectionError',
            message='Connection to the server error. Please check your connection.'
        )
    except requests.exceptions.RequestException as e:
        return ExtractionResponse(
            status='error',
            code=400,
            error='RequestException',
            message=str(e)
        )
    except Exception as e:
        return ExtractionResponse(
            status='error',
            code=500,
            error='Exception',
            message=str(e)
        )