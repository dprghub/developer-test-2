import snoop
from flask import Flask, render_template, request
from peewee import *
import datetime
from models import database_proxy, History
import requests
import requests_cache
requests_cache.install_cache(cache_name='currency_cache', backend='sqlite', expire_after=3600)

import pickle 
app = Flask(__name__)

database = SqliteDatabase('test.db')
database_proxy.initialize(database)

database.create_tables([History])

@app.route('/')
def index():
    return render_template('index.html')

@snoop
@app.route('/convert', methods=['POST'])
def convert():
    # TODO: do conversion of currency
    date = datetime.datetime.now()
    amount = request.form['amount']
    src_currency = request.form['src_currency'].upper()
    tgt_currency = request.form['tgt_currency'].upper()
    
    response = requests.get(f"https://free.currconv.com/api/v7/convert?q={src_currency}_{tgt_currency}&compact=ultra&apiKey=09cb0e075a44116bd021")
    result = response.json()[f"{src_currency}_{tgt_currency}"]
    result = float(result)*int(amount)
    history = History(result=result, tgt_amount=int(amount), src_amount=int(amount), src_currency=src_currency, tgt_currency=tgt_currency, date=date)
    history.save()

    return render_template('convert.html', result=result)

@app.route('/history')
def history(limit=25, offset=0):
    history = History.select().limit(limit).offset(offset)

    return render_template('history.html', history=history)

app.run(debug=True)
