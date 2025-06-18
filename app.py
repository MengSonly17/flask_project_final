from urllib.parse import quote_plus

from Tools.scripts.make_ctype import method
from flask import Flask , render_template , request
import requests
from tabulate import tabulate
from datetime import date
import time
from babel.numbers import format_currency
import getpass
from idna.idnadata import joining_types

app = Flask(__name__)


@app.route('/')
def home():
    try:
        products = []
        url = 'https://fakestoreapi.com/products'

        data = requests.get(url)
        products = data.json()

    except Exception as e:
        print(e)
    return render_template('views/home.html',products=products)

@app.route('/product')
def product():
    try:
        products = []
        url = 'https://fakestoreapi.com/products'

        data = requests.get(url)
        products = data.json()

    except Exception as e:
        print(e)
    return render_template('views/product.html',products=products)

@app.route('/about')
def aboutUs():
    return render_template('views/aboutus.html')

@app.route('/contact')
def contact():
    return render_template('views/contact.html')

@app.route('/cart')
def cart():
    return render_template('views/cart.html')

@app.route('/product_detail')
def product_detail():
    try:
        product_id = request.args.get('id')
        product = []
        url = f'https://fakestoreapi.com/products/{product_id}'
        data = requests.get(url)
        product = data.json()
    except Exception as e:
        print(e)
    return render_template('views/product_detail.html',product=product)

@app.errorhandler(404)
def not_found(e):
    return render_template('views/404.html'),404

@app.route('/checkout')
def checkout():
    return render_template('views/checkout.html')

@app.route('/messageToTelegram',methods=['POST'])
def messageToTelegram():
    data = request.get_json()
    size = len(data)

    token = "7792444361:AAHN8_IfWokdgSZ53iNAUnIj5Bk7kIbDRtk"
    chat_id = "@python_final624"
    cart_list = []

    for i in range(size-1):
        cart_list.append([
            data[i]['title'],
            data[i]['quantity'],
            data[i]['price']
        ])

    print(data[size-1])

    table = tabulate(cart_list, ["Item", "Qty", "Price"], tablefmt="fancy_outline")
    user_name = getpass.getuser()
    message = (
        f"<strong>Date </strong> {'':>42} : {'':<2} {date.today()}\n"
        f"<strong>Customer Name</strong> {'':>19} : {'':<2} {data[size-1]['fullName']}\n"
        f"<strong>Number  </strong> {'':>34} : {'':<2} {data[size-1]['number']}\n"
        f"<strong>Telegram Number  </strong> {'':>14} : {'':<2} {data[size-1]['telegramNumber']}\n"
        f"<strong>{'Payment Method':<32} : {'':<2} {data[size-1]['payMethod']} </strong>\n"
        f"<strong>{'Delivery Method':<34} : {'':<2} {data[size-1]['deliveryMethod']} </strong>\n"
        f"<strong>Email  </strong> {'':>39} : {'':<2} {data[size-1]['email']}\n"
        f"<strong>Address  </strong> {'':>34} : {'':<2} {data[size-1]['address']}\n"
        f"<strong>Sold by </strong> {'':>37} : {'':<2} {user_name}\n\n"
        f"<pre>{table}</pre>"
        f"\n\n<strong>{'Total':<54} : {'':<2} </strong>{format_currency(data[size-1]['totalAmount'], 'USD', locale='en_US')}\n"
        f"<strong>{'Receive':<50} : {'':<2} </strong>{format_currency(data[size - 1]['totalAmount'], 'USD', locale='en_US')}\n"
        f"<strong>{'Receive':<50} : {'':<2} </strong>{format_currency(0, 'USD', locale='en_US')}\n"
    )

    time.sleep(3)
    html = message
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={quote_plus(html)}&parse_mode=html"
    r = requests.get(url)

    return {"message": "Received!"}, 200


if __name__ == '__main__':
    app.run()
