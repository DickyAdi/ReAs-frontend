import pandas as pd
import requests

def submit_extract_request(url, files):
    try:
        response = requests.post(url, files=files)
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

def visualize(response, top_n, sentiment):
    if sentiment == 'Positive':
        df = pd.DataFrame(response['data']['positive_topics'])
    elif sentiment == 'Negative':
        df = pd.DataFrame(response['data']['negative_topics'])
    df = df.sort_values(by=['score'], ascending=False).head(top_n)
    return df
