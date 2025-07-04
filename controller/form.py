import pandas as pd
import requests
import os
from streamlit.runtime.uploaded_file_manager import UploadedFile
from config.settings import settings

def submit_extract_request(files, text_column):
    try:
        params = {'text_column' : text_column}
        response = requests.post(settings.BACKEND_URL, files=files, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {
            'status' : 'error',
            'code' : e.response.status_code,
            'error' : 'HTTPError',
            'message' : e.response.reason
        }
    except requests.exceptions.ConnectTimeout:
        return {
            'status' : 'error',
            'code' : 408,
            'error' : 'ConnectTimeout',
            'message' : 'Request timeout while connecting to the server.'
        }
    except requests.exceptions.ConnectionError:
        return {
            'status' : 'error',
            'code' : 503,
            'error' : 'ConnectionError',
            'message' : 'Connection to the server error. Please check your connection.'
        }
    except requests.exceptions.RequestException as e:
        return {
            'status' : 'error',
            'code' : 400,
            'error' : 'RequestException',
            'message' : str(e)
        }
    except Exception as e:
        return {
            'status' : 'error',
            'code' : 500,
            'error' : 'Exception',
            'message' : str(e)
        }

def validate_csv(file:UploadedFile):
    _, ext = os.path.splitext(file.name)
    if ext != ".csv" and file.size > settings.MAX_CLIENT_UPLOAD_SIZE * 1024 * 1024:
        return {
            'status' : 'error',
            'code' : 422,
            'error' : 'UnprocessableEntity',
            'message' : f'Cannot process file, either type mismatch or size > {settings.MAX_CLIENT_UPLOAD_SIZE}MB.'
        }
    return file

def get_csv_columns(file:UploadedFile):
    validated_file = validate_csv(file)
    if isinstance(validated_file, dict):
        return validated_file
    else:
        try:
            df = pd.read_csv(file, nrows=2)
            file.seek(0)
            return {
                'status' : 'success',
                'code' : 200,
                'message' : 'Validated file and extracted csv column.',
                'data' : {
                    'sample' : df,
                    'columns' : list(df.columns)
                }
            }
        except Exception as e:
            return {
                'status' : 'error',
                'code' : 500,
                'error' : 'Exception',
                'message' : str(e)
            }

def visualize(response, top_n, sentiment):
    if sentiment == 'Positive':
        df = pd.DataFrame(response['data']['positive_topics'])
    elif sentiment == 'Negative':
        df = pd.DataFrame(response['data']['negative_topics'])
    df = df.sort_values(by=['score'], ascending=False).head(top_n)
    return df
