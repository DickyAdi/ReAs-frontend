import streamlit as st
import plotly.express as px
from controller import form


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
        validate_file = form.get_csv_columns(fileUpload)
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
                st.session_state.response = form.submit_extract_request(files=files, text_column=file_columns)
                if st.session_state.response['status'] == 'error':
                    st.error(st.session_state.response['message'])

st.divider()


if st.session_state.response and isinstance(st.session_state.response, dict) and st.session_state.response.get('status') == 'success':
    top_n = st.selectbox('How many topics would you want to extract?', (10, 20, 30))
    sentiment = st.selectbox('What sentiment topic would you want to extract?', ('Positive', 'Negative'))
    count_topics = st.session_state.response['data'][sentiment.lower()]['count']
    count_valid = st.session_state.response['data']['number_valid_rows']
    total_metric, sentiment_metric = st.columns(2)
    data_container = st.columns(1)
    data_container2 = st.columns(1)
    with st.container():
        if count_valid <= 10:
            st.warning('Your data contain less than 10 row. More row is expected for better insights.')
        else:
            # row_1.append(st.info(f'Out of {count_valid} reviews, found {count_topics} {sentiment} words.'))
            sentiment_metric.metric(f'{sentiment} topics', form.get_humanize_metric(count_topics))
            total_metric.metric('Total valid reviews', form.get_humanize_metric(count_valid))
        df = form.visualize(st.session_state.response, top_n=top_n, sentiment=sentiment)
        fig = px.bar(df, x='score', y='word', orientation='h')
        placeholder_mean = px.bar(df, x='score', y='word', orientation='h')
        data_container.append((st.header('Std'),st.plotly_chart(fig, key='std')))
        data_container2.append((st.header('mean'), st.plotly_chart(placeholder_mean, key='mean')))