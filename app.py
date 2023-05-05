import sqlite3
import datetime
import streamlit as st
from streamlit_option_menu import option_menu

conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS medlog (date_given DATE UNIQUE)')

def add_data(date_given):
	c.execute(f'INSERT OR IGNORE INTO medlog(date_given) VALUES ("{date_given}")')
	conn.commit()
        
def remove_data(date_given):
    c.execute(f'DELETE FROM medlog WHERE date_given = "{date_given}"')
    conn.commit()

def read_most_recent():
       c.execute('SELECT date_given FROM medlog ORDER BY date_given DESC LIMIT 1')
       data = c.fetchall()
       return data

def clean_database():
      todaydate = datetime.date.today()
      c.execute(f'DELETE FROM medlog WHERE date_given != "{todaydate}"')
      conn.commit()

st.set_page_config(page_title="Ruby Galliprant Log", page_icon=":dog:",layout="wide")


selected = option_menu(
    menu_title=None,
    options=["Given today?","Log Dose","About"],
    icons=["clipboard-check","journal-medical","info-circle"],
    default_index=0,
    orientation="horizontal"
)
if selected == "Log Dose":
      st.subheader("Log a dose of Galliprant")
      todaydate = datetime.date.today()
      if st.button(f"Log dose for {todaydate}"):
             add_data(datetime.date.today())
             st.success(f"Added {datetime.date.today()} to the log!")
      if st.button(f"Remove logged dose for {todaydate}"):
             remove_data(datetime.date.today())
             st.success(f"REMOVED {datetime.date.today()} to the log!")
            

if selected == "Given today?":
    create_table()
    d = read_most_recent()
    success = "no"
    today = datetime.date.today()
    date_text = today.strftime("%Y-%m-%d")
    #remove commas and parenthesis from d, our database output
    d_clean = [item[0] for item in d]
    for date in d_clean:
        if date == date_text:
              success = "yes"
            # st.success("The most recent dose was given today!")
            # print("matched")
    if success == "yes":
          st.success("The most recent dose was given today!")
          st.balloons()
    else:
          st.error("Not given today!")
      

if selected == "About":
    st.title(":dog: Ruby's Galliprant Log:pill:")
    st.write("Use this webpage to see if Ruby has received her Galliprant dose for today, and log if you gave it to her.")
    st.subheader("Select an option in the menu to proceed.")
    clean_database()
    st.info("Databased cleaned!")

