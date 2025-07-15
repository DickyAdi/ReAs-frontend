import pandas as pd
from io import BytesIO
import os


from config.settings import settings

def validate_csv(file:BytesIO):
    _, ext = os.path.splitext(file.name)
    if ext != ".csv" or file.size > settings.max_size_bytes:
        return {
            'status' : 'error',
            'code' : 422,
            'error' : 'UnprocessableEntity',
            'message' : f'Cannot process file, either type mismatch or size > {settings.max_size_mb} MB.'
        }
    return file

def get_csv_columns(file:BytesIO):
    validate_file = validate_csv(file)
    if isinstance(validate_file, dict):
        return validate_file
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
                'error' : 'InternalServerError',
                'message' : str(e)
            }