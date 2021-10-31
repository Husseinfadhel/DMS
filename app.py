from flask import Flask, render_template, request, flash, url_for, redirect
from models import setup_db, Client
from forms import AddClient
app = Flask(__name__, template_folder='templates')

db = setup_db(app)


@app.route('/main', methods=['GET'])
def main():
    return render_template('main.html')


@app.route('/add/client', methods=['GET'])
def add_client():
    forms = AddClient()
    return render_template('addclient.html', form=forms)


@app.route('/add/client', methods=['POST'])
def add_client_post():
    new = Client(
        name=request.form['name'],
        address=request.form['address'],
        phone=request.form['phone']
    )
    Client.insert(new)
    flash('العميل ' + request.form['name'] + ' تم أضافته بنجاح')
    return redirect(url_for('main'))


@app.route('/client', methods=['GET'])
def client():
    query = Client.query.all()
    return render_template('client.html', query=query)
