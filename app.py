from Tools.scripts.make_ctype import method
from flask import Flask , render_template , request
import requests
import json
import babel
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
    print(data[0]['price'])
    print("type of = ",type(data))
    return {"message": "Received!"}, 200


if __name__ == '__main__':
    app.run()
