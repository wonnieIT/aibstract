import streamlit as st
from pathlib import Path
import base64
import pandas as pd
from io import StringIO
import openai
from streamlit_chat import message


# Initial page config
openai.api_key = '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'


st.set_page_config(
     page_title='Datalab Cheat Sheet',
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
    cs_sidebar()
    cs_body()

    return None

# Thanks to streamlitopedia for the following code snippet

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# sidebar

def cs_sidebar():

    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logo.png")), unsafe_allow_html=True)
    st.sidebar.header('Kakaogames Datalab cheat sheet')

    st.sidebar.markdown('Where? ❄️[Snowflake](https://uy06499.ap-northeast-2.aws.snowflakecomputing.com/oauth/authorize?client_id=oVF2zWn9aH4MEex%2FtbFkqc%2BvJvhJkQ%3D%3D&display=popup&redirect_uri=https%3A%2F%2Fapps-api.c1.ap-northeast-2.aws.app.snowflake.com%2Fcomplete-oauth%2Fsnowflake&response_type=code&scope=refresh_token&state=%7B%22browserUrl%22%3A%22https%3A%2F%2Fapp.snowflake.com%2Frlpfjsg%2Fis42076%2Fworksheets%22%2C%22csrf%22%3A%2286711015%22%2C%22isSecondaryUser%22%3Afalse%2C%22oauthNonce%22%3A%223mr412bZpJ4%22%2C%22url%22%3A%22https%3A%2F%2Fuy06499.ap-northeast-2.aws.snowflakecomputing.com%22%2C%22windowId%22%3A%220d99135a-2f39-4966-b6f4-67a196a2e682%22%7D)')

    st.sidebar.markdown('How? ⌨ [SQL](https://ko.wikipedia.org/wiki/SQL)')

    st.sidebar.markdown('What? 📉 [Our Datahub](https://dlk-datahub.kakaogames.io/)')
    st.sidebar.code('''
        어떤 데이터를 찾고 싶은지 검색해보세요.
        어디서 찾을 수 있는지, 어떤 컬럼에 있는지 확인해보세요.
    ''')

    st.sidebar.markdown('Why? 왜 안되지???')
    st.sidebar.code('''
        Q&A 사이트에 질문하세요!
    ''')

    return None

##########################
# Main body of cheat sheet
##########################

def cs_body():
    # Magic commands

    def generate_response(prompt):
        completions = openai.Completion.create (
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
            stop=None,
            temperature=0.5,
            top_p=1,
        )
    
        message = completions["choices"][0]["text"].replace("\n", "")
        return message

    st.subheader("👩🏻‍🏫 Datalab Query Assistant")
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    with st.form('form', clear_on_submit=True):
        user_input = st.text_input('퀴리를 입력하세요.', '', key='input')
        submitted = st.form_submit_button('Send')
    
    if submitted and user_input:
        output = generate_response("이 SQL 쿼리를 설명해줘. "+user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)
    
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))




    col1, col2 = st.columns(2)

    col1.subheader('유저 정보 확인')
    col1.write('account id 기반')
    col1.code('''
    select * from DG_USER_D03
    where base_ymd = '2023-05-23'
    and game_cd = '게임코드'
    and acntid = '특정 유저 아이디';
    
    ''')


    col1.write('player id 기반')
    col1.code('''
    select * from DG_USER_D03
    where base_ymd = '2023-05-23'
    and game_cd = '게임코드'
    and apiuid3 = '특정 유저 아이디';
    
    ''')

    # Display data

    col1.subheader('게임 코드 확인')
    col1.write("""
    예시
    * 에버소울의 고유 게임 코드는?
    ✔️ 게임 정보를 담고 있는 gamebi.dc_game_cd_mtr 에서 select
    ✔️ game_nm이라는 게임명 컬럼으로 검색 
    """)
    col1.code('''
select * from gamebi.dc_game_cd_mtr
where game_nm like ('%에버소울%');

select * from gamebi.dc_game_cd_mtr
where game_nm ilike ('%eversoul%');
    ''')

    # Display charts

    col1.subheader('ADID 리스트')
    col1.write("""
    예시
    * 프렌즈 샷
    - 추출 기간: 11/5 ~ 11/7 
    - 추출 조건: 신규가입유저 ADID
    - 추출 항목: ADID (OS 구분 부탁드립니다)
    ✔️ ADID 는 90으로 끝나는 테이블에서 찾는다

    """)
    col1.code('''
select game_cd, 
       adid,
       join_dt, 
       mket_cd 
from gamebi.dg_user_d90
where base_ymd between '2021-11-05' and '2021-11-07' --추출기간으로 이 부분을 변경할 것!
and game_cd = 'K-323337' --게임코드로 이 부분을 변경할 것!
and join_prd_tp_cd = 'D01' --신규 가입 유저 조건으로 (D01은 당일 가입자), 이 조건이 없을 시에는 빼기 
and mket_cd = 'apple' --(android의 경우 'google')

    ''')


    # Display text

    col1.subheader('가입 일자별  nonPU')
    col1.write("""
    예시) 
    * 프렌즈타운
    * 데이터 추출 기준 일 : 2022년 1월 16일 
    * 추출 요청  : DAU 중 아래 조건에 해당하는 유저 수 
    ㄴ2023년 4월 1일~2023년 5월 1일 가입자 중 nonPU인 유저 수
    """)
    col1.code('''

select
count(a1.acntid)
from (
select acntid from gamebi.dg_game_user_d03
where base_ymd = '2022-01-16'
and game_cd = 'K-78572'
and svr_cd = 'TOTAL'
and use_prd_tp_cd = 'D01'
and cast((join_dt + interval '9' hour) as varchar) between '2019-04-18 00:00:00' and '2019-05-31 23:59:59'
) a1
left outer join (
  select distinct acntid from gamebi.db_sale_sd01
  where base_ymd between '2016-10-25' and '2022-01-16'
  and game_cd = 'K-78572'
  ) a2
  on a1.acntid = a2.acntid
  where a2.acntid is null
  ;

    ''')
    # Display media


    col2.subheader('누적 금액')
    col2.code('''
    select apiuid_3, 
           sum(pay_amt) as cum_pay_amt, 
           sum(case when base_ymd between '2023-05-01' and '2023-06-25' then pay_amt else 0 end ) as may_june_pay_amt
    from gamebi.db_game_pay_hist
    where base_ymd between '2023-01-05' and '2023-06-25'
    and game_cd in ('K-743487', 'K-743491', 'K-750066')
    group by 1
    ''')

    # Lay out your app

    col2.subheader('최종 스테이지/전선')
    col2.code('''
    select apiuid_3, log_dt, game_mode_dtl 
    from gamebi.dg_game_play_hist03
    where base_ymd <= '2023-02-15'
    and game_cd =  'K-750066'
    and game_mode = '전선'
    and rslt_tp_cd = '21';
    ''')

    col2.write('조인해서 다른 테이블과 함께 보기')
    col2.code('''
    left join ( 
    select ~  
    ) a on a.key = b.key
    ''')


    col2.subheader('결제 이력')
    col2.write("""
    예시
    특정 기간에 프렌즈팝콘에 복귀한 31일 휴면 유저 중, 
    동일 기간에 팝콘에서 결제한 기록이 있는 유저 수 카운트
    """)
    col2.code('''
        select count(*) 
        from (
        select distinct acntid
        from gamebi.dg_user_d03
        where base_ymd between '2021-12-01' and '2021-12-31'
        and game_cd = 'K-78572'
        and join_prd_tp_cd <> 'D01'
        and use_prd_tp_cd = 'D01'
        and bdd_use_prd_tp_cd not in ('D01','D02','D03','D04','D05','D06','D07', 'D14','D21','D28','D30') 
        )a1
        inner join (
            select distinct acntid
            from gamebi.db_game_pay_hist
            where base_ymd between '2021-12-01' and '2021-12-31' 
            and game_cd = 'K-78572'
            )b1
            on a1.acntid = b1.acntid
            ;
    ''')

    # Placeholders, help, and options

    col2.subheader('구매 여부')
    col2.write("특정 기간 중, 특정 상품 코드 (여러 개 중 하나라도) 를 구매한 적이 있는 유니크 유저 수 ")
    col2.code('''
    select count(distinct acntid) 
    from gamebi.db_game_pay_hist
    where base_ymd between '2021-12-23' and '2021-12-31'
    and game_cd = 'K-323337'
    and game_prod_cd = 'popcorn_package93_ios_gem_kr' and 'popcorn_package93_aos_gem_kr' and 'popcorn_package93_one_gem_kr'
    ;
    ''')

    col2.subheader('년도별 월별 가입 연도별 AU 수 ')
    col2.code('''
    select
    join_yy_mm, count(*)
    from (
    select 
    acntid, join_dt, SUBSTR(cast(join_dt as varchar), 1, 7) as join_yy_mm
    from gamebi.dg_game_user_d03
    where base_ymd = '2021-12-31'
    and game_cd = 'K-78572'
    ) a1
    inner join (
        select distinct acntid
        from gamebi.dg_user_login_sd03
        where base_ymd between '2021-12-01' and '2021-12-31'
        and game_cd = 'K-78572'
        ) b1
        on a1.acntid = b1.acntid
        group by join_yy_mm
    ;
    ''')



    st.subheader('이용자 이탈 구간')
    st.write("""
    예시) 
    * 게임명 : 키튼팝
    * 최초 이탈한 유저 (미접속 7일 이상 경과)의 이탈 시점 최종 레벨 
    """)
    st.code('''
    select
    a1.acntid, a2.base_ymd, a2.user_lv
    from (
    select
    acntid
    , min(base_ymd) as base_ymd
    from (
    select 
    acntid
    , base_ymd
    from gamebi.dg_game_user_d03
    where base_ymd >= '2021-08-31'
    and game_cd = 'K-556653'
    and svr_cd = 'TOTAL'
    and use_prd_tp_cd = 'D14'
    ) tmp
    group by acntid
    ) a1
    inner join (
    select acntid, base_ymd, user_lv from gamebi.dg_game_user_d03
    where base_ymd >= '2021-08-31'
    and game_cd = 'K-556653'
    and svr_cd = 'TOTAL'
    ) a2
    on a1.acntid = a2.acntid and a1.base_ymd = a2.base_ymd
    ;
    ''')


    return None

# Run main()

if __name__ == '__main__':
    main()
