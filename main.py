import streamlit as st
import plotly.express as px
from controller import form

response = None
if 'response' not in st.session_state:
    st.session_state.response = None

st.title('ReAs Apps')
st.text('ReAs is a tool to extract a positive and negative topic from your list of reviews. Later on, you could use the information to enhance your product/businesses.', width='content')

st.divider()

with st.form('data_form'):
    fileUpload = st.file_uploader('Upload your file.', help='Only receives .csv file.', type=['csv'])
    submit = st.form_submit_button('Extract')

    if submit and fileUpload:
        with st.spinner('Predicting and extracting...'):
            files = {'file' : (fileUpload.name, fileUpload, fileUpload.type)}
            st.session_state.response = form.submit_extract_request('http://localhost:8000/extract', files=files)
            if st.session_state.response['status'] == 'error':
                st.error(st.session_state.response['message'])

st.divider()

top_n = st.selectbox('How many topics would you want to extract?', (10, 20, 30))
sentiment = st.selectbox('What sentiment topic would you want to extract?', ('Positive', 'Negative'))

if st.session_state.response and isinstance(st.session_state.response, dict) and st.session_state.response.get('status') == 'success':
    df = form.visualize(st.session_state.response, top_n=top_n, sentiment=sentiment)
    fig = px.bar(df, x='score', y='word', orientation='h')
    st.plotly_chart(fig)