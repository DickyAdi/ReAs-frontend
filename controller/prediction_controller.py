import pandas as pd
from millify import millify

from core import prediction_services, models

def extract_predict(file:dict, text_column:str) -> models.ExtractionResponse:
    response = prediction_services.submit_extract_request(file, text_column)
    return response

def get_sentiment_number(response:models.ExtractionResponse) -> tuple[int, int]:
    pos = humanize_value(response.data['positive']['count'])
    neg = humanize_value(response.data['negative']['count'])
    return pos, neg

def humanize_value(value:int) -> str:
    return millify(value, precision=2)

def get_df(response:models.ExtractionResponse, top_n:int, sentiment:str) -> tuple[pd.DataFrame, pd.DataFrame]:
    sentiment = sentiment.lower()
    sentiment_data = response.data[str(sentiment)]
    df_trend = pd.DataFrame(sentiment_data['trend_topics']).sort_values(by=['score'], ascending=False).head(top_n)
    df_frequent = pd.DataFrame(sentiment_data['frequent_topics']).sort_values(by=['score'], ascending=False).head(top_n)
    return df_trend, df_frequent