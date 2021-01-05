import requests
from bs4 import BeautifulSoup
import smtplib

URL = 'amazon.ca/'                                 # Enter your amazon link
PRICE_VALUE = 1000                                  # Enter the desired product price
SENDING_EMAIL = 'sendingaccount@gmail.com'          # Email that your want to create the notification
SENDING_EMAIL_PASSWORD = 'password'                 # Sending email's password
RECEIVING_EMAIL = 'receivingaccount@gmail.com'      # Receiving email

headers = {
    'content-type': 'text/html;charset=UTF-8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    # Enter your user agent into the quotations - google: 'my user agent'
    'User-Agent': '',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

resp = requests.get(URL, headers=headers)

soup = BeautifulSoup(resp.content, 'lxml')


def trackPrices():
    price = float(getPrice(URL))
    # print(price)
    if price > PRICE_VALUE:
        diff = float(price - PRICE_VALUE)
        print(f"Still ${diff} too expensive")
    else:
        print("Cheaper! Sending Notification To Your Email...")
        sendEmail()
    pass


def getPrice(url):
    # Array-slice may have to be modified to work with the products price
    price = soup.find('span', id='priceblock_ourprice').text.strip()[1:]
    return price


def sendEmail():
    title = soup.find('span', id='productTitle').text.strip()
    subject = f"Amazon Price for {title} Has Dropped!"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(SENDING_EMAIL, SENDING_EMAIL_PASSWORD)

    body = f'Check the amazon link: {URL}'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(RECEIVING_EMAIL, RECEIVING_EMAIL, msg)

    print('Email has been sent')


trackPrices()

