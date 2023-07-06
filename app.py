import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, show_pages, add_page_title
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
import time
import openai
import altair as alt
import ast 
import os 

openai.api_key = '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'



add_selectbox = st.sidebar.selectbox(
    "게임을 선택하세요",
    ("우마무스메", "오딘", "아키에이지워", "가디언테일즈")
)

# Using "with" notation
with st.sidebar:
    limit = st.radio(
        "최근 데이터 수",
        ("10", "50")
    )
    board_type = st.radio(
        "게시판 종류",
        ("건의","자유")
    )
    show = st.button("결과 보기")

if show:
    st.header(f'🤖{add_selectbox} {board_type} 게시판 by Aibstract ')    

    col1, col2 = st.columns(2)
    if board_type=="건의":
        bdex= 1
    else:
        bdex=2


    mappings = {
        "우마무스메" : ["umamusume-kor", "ZaXF", "Z4oy", "https://img1.daumcdn.net/thumb/C151x151/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1ZK1D%2F5c0477e8a6bfb94974136c978f5e2522dc17b29e"],
        "오딘" : ["odin", "DEIV", "D034", "https://img1.daumcdn.net/thumb/C151x151/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1YvZ5%2Fabe49aa5aeb26dc71c157eef3bcf105bac519759"],
        "아키에이지워" : ["ArcheAgeWar", "aaTV","ZmF6", "https://img1.daumcdn.net/thumb/C151x151/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1ZOrf%2F26e8c4ce3b61a009d776c42eeadb7646e250f494"],
        "에버소울": ["Eversoul", "aCex", "Zkxr", "https://img1.daumcdn.net/thumb/C151x151/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1ZLyF%2F2d4d47292e41f06e4163d2f20a9a66bca6394c3e"],
        "가디언테일즈": ["GuardianTales","AgPy","ARz6","https://img1.daumcdn.net/thumb/C151x151/?fname=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1YmAL%2F2fbe0cff9c7614a9f7750edb31a9735b37bd14a8"]
    }
    
    limit_map = {
        "10": "1",
        "20": "2",
        "30": "3",
        "40": "4",
        "50": "5"
    }

    @st.cache_data
    def get_raw_data(cafe_name, req_board_name, limit):
        driver = webdriver.Chrome()
        page = driver.get(f'https://cafe.daum.net/{cafe_name}/{req_board_name}')
        driver.switch_to.frame("down")
        driver.find_element(By.XPATH,'//*[@id="primaryContent"]/div/div[1]/div[2]/div[3]/div[1]/label').click()
        time.sleep(2)

        driver.find_element(By.XPATH,'//*[@id="primaryContent"]/div/div[1]/div[2]/div[3]/div[2]/a').click()
        time.sleep(2)

        driver.find_element(By.XPATH,f'//*[@id="primaryContent"]/div/div[5]/div[2]/div/div[{limit}]/a').click()
        time.sleep(2)


        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser') 
        profile = soup.select('#cafeProfileImage > img')[0]['src']


        post_titles = soup.find_all('a', {'class': 'txt_item'})
        article_num = soup.find_all('div',{'class':'wrap_num'})
        views = soup.find_all('span', {'class': 'tbl_txt_look'})
        rec_counts = soup.find_all('span',{'class':'tbl_txt_recommend'})
        dates = soup.find_all('td',{'class': 'td_date'})
        writer = soup.find_all('td',{'class': 'td_writer'})
        recomm =[]
        titles = []
        clicks = []
        article_id = []
        regdate = []
        author = []
        for ele in rec_counts:
            recomm.append(ele.get_text())

        for ele in views:
            clicks.append(ele.get_text())

        for ele in article_num:
            article_id.append(ele.get_text())

        for ele in post_titles:
            titles.append(ele.get_text())

        for e in writer:
            author.append(e.get_text())
        for e in dates:
            if str(e.get_text()).startswith('23.') == False:
                today = date.today().strftime("%y.%m.%d")
                regdate.append(today)
            else:
                regdate.append(e.get_text())
        data = { 'id': article_id, 'titles' : titles, 'recommendations': recomm, 'views': clicks , 'regdate': regdate, 'author':author}
        df = pd.DataFrame(data)
        df['views'] =  pd.to_numeric(df['views'])
        df['link'] = f'https://cafe.daum.net/{cafe_name}/{req_board_name}/' + df['id']
        return df


    def get_answers_from_gpt(command,temp):
        completion = openai.ChatCompletion.create (

        model = 'gpt-3.5-turbo-0613',
        messages = [{"role": "user", "content": command}],
        temperature=temp
        )
        return completion['choices'][0]['message']['content']


    @st.cache_data  
    def add_specific_contents(df):
        driver = webdriver.Chrome()
        contents = []
        for index, row in df.iterrows():
            url = df.iloc[index]['link']
            page = driver.get(url)
            driver.switch_to.frame("down")
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser') 
            if len(soup.select('#user_contents')) == 0 :
                contents.append('')
            else :
                texts = soup.select('#user_contents')[0].get_text()
                contents.append(texts.replace(u'\xa0', u' ').lstrip())
        df['contents']=contents
        return contents
    

    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    @st.cache_data
    def add_summary(df):
        summary = []
        for ele in df['contents']:
            command = f"""
                아래의 건의사항을 한문장으로 요약해줘. 
                {ele}
                """
            completion = openai.ChatCompletion.create (

                model = 'gpt-3.5-turbo-0613',
                messages = [{"role": "user", "content": command}]
                
                )
            summary.append(completion['choices'][0]['message']['content'])
        df['summary'] = summary
        return df



    if add_selectbox in ("에버소울","가디언테일즈"):
        df = get_raw_data(mappings[add_selectbox][0],mappings[add_selectbox][bdex], limit_map[limit])
        add_specific_contents(df)
        add_summary(df)
        sent_cmd = f"""

                아래 전달하는 list는 게임 건의 제목인데, 각각 sentiment analysis를 해서 -1과 1 사이의 값을 설명 없이 length가 50인 python list로 설몀 없이  전달해줘. 

                {df['titles']}
                """
        sentiments = get_answers_from_gpt(sent_cmd,0.5)
        sentiments=ast.literal_eval(sentiments)
        print(sentiments)
        if len(sentiments) ==50:
            df['sentiments'] = sentiments
        df.to_csv(f'{mappings[add_selectbox][0]}-{mappings[add_selectbox][bdex]}.csv')

    else: 
        df = pd.read_csv(f'{mappings[add_selectbox][0]}-{mappings[add_selectbox][bdex]}.csv')

    add_logo(mappings[add_selectbox][3])
    # TOO SLOW 
    # if board_type == '자유':
    #     df = get_raw_data(mappings[add_selectbox][0],mappings[add_selectbox][2], limit_map[limit])
    #     add_specific_contents(df)
    #     add_summary(df)
    # else:
    #     df = get_raw_data(mappings[add_selectbox][0],mappings[add_selectbox][1], limit_map[limit])
    #     add_specific_contents(df)
    #     add_summary(df)
    # Streamlit UI 



    # sent_cmd = f"""

    # 아래 전달하는 list는 게임 건의 제목이야.
    # 각각의 sentiment analysis를 해서 -1과 1 사이의 값을 설명 없이 length가 list와 동일한 python list로 전달해줘. 

    # {df['titles']}
    # """
    # sentiments = get_answers_from_gpt(sent_cmd,0.3)
    # sentiments=ast.literal_eval(sentiments)
    # print(sentiments)
    # df['sentiments'] = sentiments

    date_count = df.groupby(df['regdate']).size().reset_index(name='Count')
    
    st.markdown(f"### {board_type} 게시판 5가지 시사점")
    issues = get_answers_from_gpt(f"""
            아래는 건의함 내용들인데 주요 건의 사항 5가지로 요약하고 시사점을 알려줘.  
            {df['titles']}
            """, 0.8)
    st.write(issues) 


    hot_issues = df.sort_values(by=['views','recommendations'],ascending=False)[:10]
    st.markdown("### 조회수, 추천수 높은!")
    st.write(hot_issues[["titles","summary","link"]]) 


    with col1:
        st.markdown("### 등록 글 현황")
        st.line_chart(date_count, x='regdate',y='Count')

        

  

    with col2:
        st.markdown("### 빈도 높은 키워드")
        keywords = get_answers_from_gpt(f"""
        아래는 게임 건의함 내용들인데 빈도가 높은 단어 다섯가지와 빈도 퍼센트를 알려줘.
        {df['titles']}
        """, 0.8)
        st.write(keywords) 


    st.markdown("### 최근 데이터")
    csv = convert_df(df)
    st.download_button(
        label="csv로 다운받기",
        data=csv,
        file_name=f'{mappings[add_selectbox][0]}-{mappings[add_selectbox][bdex]}.csv',
        mime='text/csv',
    )
    st.write(df[['id','titles','contents','regdate','summary','sentiments','author','link']])

    st.markdown("### Sentiment Analysis")
    sentiment_count = df.groupby(df['sentiments']).size().reset_index(name='Count')
    s_data = alt.Chart(df[["sentiments","regdate",'titles']]).mark_circle().encode(
        x='regdate', y='sentiments', size='sentiments', color='sentiments')
    st.altair_chart(s_data, use_container_width=True)

  
