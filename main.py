import streamlit as st


pages = {
    "Analysis": [
        st.Page("pages/correlation_page.py", title="Stock-Commodity Correlation"),
        st.Page("pages/page.py", title="Page"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
