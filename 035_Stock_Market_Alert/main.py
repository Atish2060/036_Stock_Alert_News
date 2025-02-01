import requests
from twilio.rest import Client
STOCK = "NVDA"

#API of the website
API_KEY = "Your API Key of the Site"

#Account token and if foe twillio
account_sid = "Your Account SID"
auth_token = "Your Auth Token"
client = Client(account_sid, auth_token)

parameters ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize":"compact",
    "apikey": API_KEY,

}
parameters1={
    "function":"NEWS_SENTIMENT",
    "tickers":STOCK,
    "apikey":API_KEY
}

#getting the information of the NVDIA stock from the API of Alphavantage
stock_response = requests.get(url="https://www.alphavantage.co/query",params=parameters)
stock_response.raise_for_status()
data = stock_response.json()
dict_data = data["Time Series (Daily)"]
list_data = []
for keys in dict_data:
    list_data.append(keys)

day1 = list_data[0]
day2 = list_data[1]
data_day1 =float(data["Time Series (Daily)"][day1]["4. close"])
data_day2 = float(data["Time Series (Daily)"][day2]["4. close"])
difference = data_day1-data_day2
percentage = (difference/data_day2) * 100
rounded_percentage = round(percentage, 2)

#Getting the information from the API related to the news of NVDIA Corp from Alphavantage
news_response = requests.get(url="https://www.alphavantage.co/query", params=parameters1)
news_response.raise_for_status()
data_news = news_response.json()
news1 = data_news["feed"][0]["title"]
summary1 = data_news["feed"][0]["summary"]
news2 = data_news["feed"][1]["title"]
summary2 = data_news["feed"][1]["summary"]
news3 = data_news["feed"][2]["title"]
summary3 = data_news["feed"][2]["summary"]

#Sending the message in whatsapp through the use of Twilio
if rounded_percentage > 0:
    message = client.messages.create(
        from_="whatsapp:Twilio generated number",
        body=f"NVDA: 🔺{rounded_percentage}%\nHeadline:{news1}\nBrief:{summary1}\n\n"
             f"NVDA: 🔺{rounded_percentage}%\nHeadline:{news2}\nBrief:{summary2}\n\n"
             f"NVDA: 🔺{rounded_percentage}%\nHeadline:{news3}\nBrief:{summary3}\n\n",
        to="whatsapp:Number to send"
    )
    print(message.status)
elif rounded_percentage < 0:
    message = client.messages.create(
        from_="whatsapp:Twilio generated number",
        body=f"NVDA: 🔻{rounded_percentage}%\nHeadline:{news1}\nBrief:{summary1}\n\n"
             f"NVDA: 🔻{rounded_percentage}%\nHeadline:{news2}\nBrief:{summary2}\n\n"
             f"NVDA: 🔻{rounded_percentage}%\nHeadline:{news3}\nBrief:{summary3}\n\n",
        to="whatsapp:Number to send"
    )
    print(message.status)

