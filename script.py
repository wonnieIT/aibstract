import streamlit as st
from st_pages import Page, show_pages, add_page_title

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    
    [  
     
        Page("contents.py", '2023 July Project',"☀️"),
        Page("app.py", "Aibstract","🎮"),
        Page("cheatsheet.py", "etc","👀")
    ]
)

