import requests
import pandas as pd
from stocksymbol import StockSymbol
from bs4 import BeautifulSoup
from email.message import EmailMessage
import ssl
import smtplib
import schedule
import time

url = 'https://hindenburgresearch.com/'

headers = {
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',    'Accept-Language':'en-GB,en;q=0.5',
    'Referer':'https://google.com',
    'DNT':'1',
}

api_key = "API KEY FROM 'https://stock-symbol.herokuapp.com/'"
ss = StockSymbol(api_key)
symbol_list_us = ss.get_symbol_list(market="US")
df_1 = pd.DataFrame(symbol_list_us)
lst = list(df_1["longName"])


print('running')
time.sleep(5)
while True:
    try: 
        r = requests.get(url, headers = headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        row = soup.find('div', class_='row')
        old_headline = row.h1.text

        time.sleep(5)
            
        r = requests.get(url, headers = headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        row = soup.find('div', class_='row')
        new_headline = row.h1.text

        if old_headline == new_headline:
            continue

        else:           
            r = requests.get(url, headers = headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            row = soup.find('div', class_='row')
            headline = row.h1.text
            
            colon = [z for z, letter in enumerate(headline) if letter == ":"]
            company_name = headline[:colon[0]].title()
            index = [company_name in item for item in lst].index(True)
            ticker = df_1['symbol'][index]

            #Must connect to Gmail API
            email_sender = 'YOUR EMAIL'
            email_password = 'PASSWORD FROM GMAIL API'
            email_receiver = 'EMAIL RECIPIENT'

            subject = "Hindenberg Header Change"
            body = "Hindenberg Updated Headline -  " + str(headline) + " - Ticker: " + str(ticker)


            em = EmailMessage()
            em['From'] = email_sender
            em["To"] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())
                print("Email Sent")
                print('Headline: ' + str(headline))
                print('Company Name: ' + str(company_name))
                print('Ticker:' + str(ticker))

            time.sleep(5)
            continue

    except Exception as e:
        print("error")
