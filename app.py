from logging import debug
from urllib.parse import quote_plus
from flask import Flask , render_template , request
import requests
from tabulate import tabulate
from datetime import datetime
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
    now = datetime.now()
    dateTime = now.strftime("%d/%m/%Y %H:%M:%S")
    table = tabulate(cart_list, ["Item", "Qty", "Price"], tablefmt="fancy_outline")
    message = (
        f"<strong>✅ Checkout Summary </strong>\n\n"
        f"<strong>📅 Date </strong> {'':>32} : {'':<2} {dateTime}\n"
        f"<strong>🕵️‍♂️ Customer Name</strong> {'':>9} : {'':<2} {data[size-1]['fullName']}\n"
        f"<strong>📱 Number  </strong> {'':>24} : {'':<2} {data[size-1]['number']}\n"
        f"<strong>📬 Email  </strong> {'':>29} : {'':<2} {data[size-1]['email']}\n"
        f"<strong>📍 Address  </strong> {'':>24} : {'':<2} {data[size-1]['address']}\n"
        f"<strong>💳 {'Payment Method':<22} : {'':<2} {data[size-1]['payMethod']} </strong>\n"
        f"<strong>🚚 {'Delivery Method':<24} : {'':<2} {data[size-1]['deliveryMethod']} </strong>\n\n"
        f"<pre>{table}</pre>"
        f"\n\n<strong>{'💰 Total':<13} : {'':<2} </strong>{format_currency(data[size-1]['totalAmount'], 'USD', locale='en_US')}\n"
        f"<strong>{'✅ Receive':<5} : {'':<2} </strong>{format_currency(data[size - 1]['payment'], 'USD', locale='en_US')}\n"
        f"<strong>{'💵 Change':<5} : {'':<2} </strong>{format_currency(float(data[size - 1]['payment'])-float(data[size-1]['totalAmount']), 'USD', locale='en_US')}\n"
    )

    time.sleep(2)
    html = message
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={quote_plus(html)}&parse_mode=html"
    r = requests.get(url)

    return {"message": "Received!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
