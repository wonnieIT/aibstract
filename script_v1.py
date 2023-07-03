import streamlit as st
from streamlit_extras.app_logo import add_logo
from st_pages import Page, Section, show_pages, add_page_title
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
import openai

add_page_title() # By default this also adds indentation

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [   Section("2023 July Project", icon="🎈️"),
        Page("script_v1.py", "Intro", "🏠"),
        Section("Games", icon="🎮"),
        Page("./games/umamusume.py", "우마무스메", "🧚🏻‍♀️"),
        Page("./games/odin.py", "오딘", "🧞‍♀️"),
        Page("./games/aki.py", "아케이에지 워", "🛠")
    ]
)


