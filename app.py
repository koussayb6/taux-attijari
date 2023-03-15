from datetime import datetime
import requests
from bs4 import BeautifulSoup
import smtplib
import streamlit as st
import threading
import json

# define the path to the file
file_path = 'previous.json'

def my_task():
    st.info("task")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []
    div = soup.find('div', attrs={'class': 'div_tab margin_bottom30'})
    table = div.find('table')
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    for d in data:
        if d[1] == 'EUR':
            current_amount = float(d[4])
    # Initial amount
    # read data from file
    with open(file_path, 'r') as f:
        loaded_data = json.load(f)
    # Compare the current amount to the previous amount
    if current_amount < loaded_data:
        # Send an email notification
        st.info("sending: " + str(datetime.now()))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = 'Amount changed!'
            body = f'The amount is now {current_amount}'
            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(EMAIL_ADDRESS, 'boussetta.koussay@gmail.com', msg)

        # Update the previous amount
        data = current_amount
        with open(file_path, 'w') as f:
            json.dump(data, f)
        st.info('sent')
    # schedule the next run in 10 minutes
    threading.Timer(6, my_task).start()


st.title('scrap euro/tnd rate')
# Email settings
EMAIL_ADDRESS = 'kousssayb6@gmail.com'
EMAIL_PASSWORD = st.secrets["gmail_app_password"]

# Web page settings
URL = 'https://www.attijaribank.com.tn/Fr/Cours_de_change__59_205'

my_task()
