import requests
from bs4 import BeautifulSoup
import smtplib
from secrets import secrets

sending_email = secrets['sending_email']
sending_password = secrets['sending_password']
receiving_email = secrets['receiving_email']

PRODUCT_PAGE = 'https://www.amazon.com/ChefSteps-Joule-Watts-White-Stainless/dp/B01M8MMLBI/ref=sr_1_4?dchild=1&keywords=joule&qid=1619292897&sr=8-4'
alert_price = 200.0
head = {
    'Accept-Language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7,ko-KR;q=0.6,ko;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

response = requests.get(PRODUCT_PAGE,
                        headers=head)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
price = float(soup.find('span', id='price_inside_buybox').getText().split('$')[1])

if price < alert_price:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        print('sending...')
        connection.starttls()
        connection.login(user=sending_email, password=sending_password)
        connection.sendmail(
            from_addr=sending_email,
            to_addrs=receiving_email,
            msg=f'Subject: Price Alert\n\nJoule is ${price}, ${alert_price - price} lower than your alert value!')
