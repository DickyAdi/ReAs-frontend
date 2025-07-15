import streamlit as st
import plotly.express as px

from controller import csv_controller, prediction_controller


top_n = 10
sentiment = 'Positive'

if 'response' not in st.session_state:
    st.session_state.response = None

st.title('ReAs Apps')
st.text('ReAs is a tool to extract a positive and negative topic from your list of reviews. Later on, you could use the information to enhance your product/businesses.', width='content')

st.divider()

fileUpload = st.file_uploader('Upload your file.', help='Only receives .csv file and ensure the file contains review text.', type=['csv'])
if fileUpload:
    with st.spinner('Validating and checking your file.'):
        validate_file = csv_controller.get_csv_columns(fileUpload)
        if validate_file.get('status') == 'error':
            st.error(validate_file['message'])

if fileUpload and validate_file.get('status') != 'error':
    with st.form('data_form'):
        st.dataframe(validate_file['data']['sample'])
        file_columns = st.selectbox('Choose text review column based on your data above.', options=validate_file['data']['columns'])
        submit = st.form_submit_button('Extract')

        if submit:
            with st.spinner('Predicting and extracting...'):
                files = {'file' : (fileUpload.name, fileUpload, fileUpload.type)}
                st.session_state.response = prediction_controller.extract_predict(file=files, text_column=file_columns)
                if st.session_state.response.status == 'error':
                    st.error(st.session_state.response.message)

st.divider()


if st.session_state.response and st.session_state.response.status == 'success':
    top_n = st.selectbox('How many topics would you want to extract?', (10, 20, 30))
    sentiment = st.selectbox('What sentiment topic would you want to extract?', ('Positive', 'Negative'))
    # count_topics = st.session_state.response['data'][sentiment.lower()]['count']
    n_positive, n_negative = prediction_controller.get_sentiment_number(st.session_state.response)
    count_valid = st.session_state.response.data['number_valid_rows']
    total_metric, positive_metric, negative_metric = st.columns(3)
    data_container = st.columns(1)
    data_container2 = st.columns(1)
    with st.container():
        if count_valid <= 10:
            st.warning('Your data contain less than 10 row. More row is expected for better insights.')
        else:
            positive_metric.metric(f'Positive sentiments', n_positive)
            negative_metric.metric(f'Negative sentiments', n_negative)
            total_metric.metric('Total valid reviews', prediction_controller.humanize_value(count_valid))
        df_trend, df_frequent = prediction_controller.get_df(st.session_state.response, top_n=top_n, sentiment=sentiment)
        trend_fig = px.bar(df_trend, x='score', y='word', orientation='h')
        frequent_fig = px.bar(df_frequent, x='score', y='word', orientation='h')
        data_container.append(
            (st.header('Trending topics'),
            st.caption("This figure highlights topics that are not only frequently mentioned, but also show strong spikes in attention across reviews. A high score means this topic is being discussed intensely in bursts. Useful for spotting emerging praise or recurring complaints."),
            st.plotly_chart(trend_fig, key='std')))
        data_container2.append(
            (st.header('Commonly Discussed'),
            st.caption('This figure shows which topics people talk about the most across all reviews. A higher score means the topic is mentioned frequently and consistently, highlighting what matters most to customers overall.'),
            st.plotly_chart(frequent_fig, key='mean')))