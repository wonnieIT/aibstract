import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, show_pages, add_page_title
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import openai

openai.api_key = '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'
with st.spinner('Loading.. Data...'):
    time.sleep(10)
st.success('Done!')


recomm =[]
titles = []
clicks = []
article_id = []
regdate = []

CAFE_NAME = 'umamusume-kor' 
REQ_BOARD_NAME = 'ZaXF' 

@st.experimental_singleton
def get_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

options = Options()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
driver = get_driver()



# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)

page = driver.get(f'https://cafe.daum.net/umamusume-kor/{REQ_BOARD_NAME}')

driver.switch_to.frame("down")
driver.find_element(By.XPATH,'//*[@id="primaryContent"]/div/div[1]/div[2]/div[3]/div[1]/label').click()
time.sleep(2)

driver.find_element(By.XPATH,'//*[@id="primaryContent"]/div/div[1]/div[2]/div[3]/div[2]/a').click()
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="primaryContent"]/div/div[5]/div[2]/div/div[5]/a').click()
time.sleep(2)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser') 
profile = soup.select('#cafeProfileImage > img')[0]['src']
add_logo(profile)
post_titles = soup.find_all('a', {'class': 'txt_item'})
article_num = soup.find_all('div',{'class':'wrap_num'})
views = soup.find_all('span', {'class': 'tbl_txt_look'})
rec_counts = soup.find_all('span',{'class':'tbl_txt_recommend'})
dates = soup.find_all('td',{'class': 'td_date'})


for ele in rec_counts:
    recomm.append(ele.get_text())

for ele in views:
    clicks.append(ele.get_text())

for ele in article_num:
    article_id.append(ele.get_text())

for ele in post_titles:
    titles.append(ele.get_text())

for e in dates:
    regdate.append(ele.get_text())

data = { 'id': article_id, 'titles' : titles, 'recommendations': recomm, 'views': clicks, 'regdate': regdate}

df = pd.DataFrame(data)

# Streamlit UI 
st.title('우마무스메 공식카페 분석')

st.write("Recent Raw Data... ")
st.write(df)


list_of_titles= '\n'.join(titles)

contents = f"""

아래는 건의함의 게시글 리스트야. 시사점 5가지를 알려줘. 
{list_of_titles}

"""


completion = openai.ChatCompletion.create (

    model = 'gpt-3.5-turbo-0613',
    messages = [{"role": "user", "content": contents}],
    temperature=0.8
)


st.markdown("### 건의함 5가지 시사점🎈")
st.text(completion['choices'][0]['message']['content'])
