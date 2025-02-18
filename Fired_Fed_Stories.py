import streamlit as st
import pandas as pd

#Connect to snowflake
conn = st.connection("snowflake")
df = conn.query("SELECT * FROM ffs_view;", ttl="10m")

#Init
pd_df = pd.DataFrame(df)
pd_df.columns = ['Shared Stories']
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

max_size = pd_df.shape[0]

st.write("# Welcome to Fired Fed Stories")

st.markdown(
    """
    Beginning on January 20, 2025, federal employees began to be subject to illegal terminations. 
    To date, this culminated on the weekend of February 14th, 
    where thousands of probationary federal employees across the country were illegally terminated 
    due to claims of poor performance.  
    
    Probationary federal employees, and other illegally terminated federal employees - 
    we want to hear your stories. 
    We want to hear why you joined public service. 
    We want to hear what type of work you were doing, 
    and what that work meant to you. 
    And we want to know how you were illegally terminated.  

    These stories are not being collected for lawsuits nor media coverage. 
    This stories are being collected so the humans behind public service can share their truth with anyone willing to listen.
"""
)

st.markdown(
    """
    If you are an illegally terminated federal employee, your story deserves to be heard.  

    Please feel free to share your story [here](https://docs.google.com/forms/d/e/1FAIpQLSdRVJ-0tJKJoOwV-Dyw4avaDF790t7yg5_tctW4fwa_GTDPWw/viewform?usp=dialog)!
""")
st.divider()
st.write(f"# Stories submitted so far: {max_size}")

pagination = st.container()

#Shout out: https://medium.com/streamlit/paginating-dataframes-with-streamlit-2da29b080920
bottom_menu = st.columns((4, 1, 1))
with bottom_menu[2]:
    batch_size = st.selectbox("Page Size", options=[5, 10, 15])
with bottom_menu[1]:
    total_pages = (
        int(len(pd_df) / batch_size) if int(len(pd_df) / batch_size) > 0 else 1
    )
    current_page = st.number_input(
        "Page", min_value=1, max_value=total_pages, step=1
    )
with bottom_menu[0]:
    st.markdown(f"Page **{current_page}** of **{total_pages}** ")

pages = split_frame(pd_df, batch_size)
pagination.table(data=pages[current_page - 1])