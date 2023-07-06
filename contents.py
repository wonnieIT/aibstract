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
    st_lottie(url_json, width =300)

with col2:
    st.subheader('AIbstract를 소개합니다')
    st.write("""
    AI + Abstract 를 줄임말으로 
    AI가 공식 웹사이트를 요약해주는 서비스입니다.😄 
    게임 운영에 있어 사람들의 의견이 무엇인지 반영하는 것은 
    중요해보이는데요!! 공식 웹사이트 데이터를 반영하려고 하는데, 
    일일이 들어가기 번거롭거나 한 곳에 모아서 보고 싶을 때! 부족하지만,, 저를 찾아주세요. 
    """)

with col3:
    st.markdown(
        """
        ### 🎈 Motivation
        * 게임 유저들의 피드백 데이터를 활용해보고 싶다.
        * GPT 활용해보고 싶다.
            * 보이지는 않지만 나보다 더 빨리 코딩...?
        * 재밌는 UI 기능 활용해보고 싶다. 
            * [streamlit 공식 문서](https://docs.streamlit.io/).
    """)
    
with col4: 

    st.markdown("""
        ### ⏰ Process
        1. Test 과정 
        * 웹 스크랩 test 
        * 데이터 확인 
        * GPT API 사용 test 
        * UI 구현 test 

        2. 컨텐츠 정리
        
        3. Code 를 Application 으로 .. 😳
        
        """)
st.markdown("""

    ### ✍️ Final Thoughts
    - db가 없어서 데이터 한정적, slow 
    - streamlit 되게 편해서 좋았다, streamlit snowflake와 연동해서 간단한 app 구축 가능성 확인
    - gpt의 요약 기능 👍🏻, 하지만 상세한 분석은 ...？
    

    """)



result = st.button("Let's get started!!")
if result:
    st.balloons()