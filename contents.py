import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, show_pages, add_page_title
from selenium import webdriver
from selenium.webdriver.common.by import By
from streamlit_timeline import timeline
import json
import requests
from streamlit_lottie import st_lottie

add_logo("main.png")
st.title("2023 July Project - Wonnie")
url = requests.get(
    "https://assets1.lottiefiles.com/packages/lf20_G6Lxp3nm1p.json")
# Creating a blank dictionary to store JSON file,
# as their structure is similar to Python Dictionary
url_json = dict()

if url.status_code == 200:
    url_json = url.json()
else:
    print("Error in the URL")


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
with col1:
    st_lottie(url_json, width =350)

with col2:
    st.subheader('👋🏻AIbstract를 소개합니다')
    st.write("""
    **AI + Abstract**의 줄임 말으로 
    AI가 공식 웹사이트를 요약해주는 서비스입니다.😄 
    물론 로그와 정형화된 데이터도 중요하겠지만, 유저들이 공식 홈페이지에 작성하는 의견들도 꽤 게임을 운영하고
    이탈을 방지하는 데에 중요해 보이는데요...""")
    st.write("✔️ 이런 비정형 데이터를 로그와 함께 분석에 활용하고 싶거나 여론을 확인하고 싶을 때!")
    st.write("✔️ 일일이 사이트에 파도타고 들어가기 번거롭거나 한 곳에 모아서 보고 싶을 때! ")
    st.write("부족하지만,, 저를 찾아주세요")

with col3:
    st.markdown(
        """
        ### 🎈 Motivation
        * 게임 유저들의 피드백 데이터를 활용해보고 싶다.
            * 꽤나 이탈 방지에 중요한 비정형 데이터...?  
        * GPT 활용해보고 싶다.
            * 보이지는 않지만 나보다 더 빨리 코딩...?
        * 재밌는 low-code UI 만들어 보고 싶다. 
            * [streamlit 공식 문서](https://docs.streamlit.io/).
            * [UI 비교](https://plotly.com/comparing-dash-shiny-streamlit/)

    """)
    
with col4: 

    st.markdown("""### ⏰ Tools """) 
    st.markdown("""
        * only 🐍PYTHON🐍
        * Libraries: selenium, streamlit, pandas, openai 📚 
        * Open AI key🔑  
        * Deployment: Github
            > 추후에 개발된다면 k8s!              
        """)
    
st.markdown("""

    ### ✍️ Final Thoughts
    - db가 없어서 데이터 한정적, slow 
    - streamlit 되게 편해서 좋았다, streamlit snowflake와 연동해서 간단한 app 구축 가능성 확인
    - gpt의 요약 기능 👍🏻, 하지만 상세한 분석은 ...？ 
        - 어떻게 한지도 모르겠고,, 가끔 직관적으로 맞지 않기도
    

    """)



result = st.button("Let's get started!!")
if result:

    st.balloons()
