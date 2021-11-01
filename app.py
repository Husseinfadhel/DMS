from flask import Flask, render_template, request, flash, url_for, redirect
from models import setup_db, Client, Driver, Masareef
from forms import AddClient, Search, AddDriver, AddMasrf

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
    form = Search()
    return render_template('client.html', query=query, form=form)


@app.route('/client', methods=['POST'])
def client_post():
    search = request.form['search']
    form = Search()
    filte = Client.query.filter(db.or_(
        Client.name.like('%{}%'.format(search)),
        Client.phone.like('%{}%'.format(search)),
        Client.address.like('%{}%'.format(search))
    ))
    return render_template('client.html', query=filte, form=form)


@app.route('/add/driver', methods=['GET'])
def add_driver():
    driver = AddDriver()
    return render_template('addriver.html', form=driver)


@app.route('/add/driver', methods=['POST'])
def add_driver_post():
    new = Driver(name=request.form['name'],
                 phone=request.form['phone'],
                 card_no=request.form['card_no']
                 )
    Driver.insert(new)
    return redirect(url_for('main'))


@app.route('/driver', methods=['GET'])
def driver():
    query = Driver.query.all()
    form = Search()
    return render_template('driver.html', query=query, form=form)


@app.route('/driver', methods=['POST'])
def driver_post():
    search = request.form['search']
    form = Search()
    filte = Driver.query.filter(db.or_(
        Driver.name.like('%{}%'.format(search)),
        Driver.phone.like('%{}%'.format(search)),
        Driver.card_no.like('%{}%'.format(search))
    ))
    return render_template('driver.html', query=filte, form=form)


@app.route('/add/masrf', methods=['GET'])
def add_masrf():
    masrf = AddMasrf()
    return render_template('addmasaref.html', form=masrf)


@app.route('/add/masrf', methods=['POST'])
def add_masrf_post():
    new = Masareef(reason=request.form['reason'],
                   amount=request.form['amount'],
                   date=request.form['date']
                   )
    Masareef.insert(new)
    return redirect(url_for('main'))

@app.route('/masrf', methods=['GET'])
def masrf():
    query = Masareef.query.all()
    form = Search()
    return render_template('masrf.html', query=query, form=form)


@app.route('/masrf', methods=['POST'])
def masrf_post():
    search = request.form['search']
    form = Search()
    filte = Masareef.query.filter(db.or_(
        Masareef.reason.like('%{}%'.format(search)),
        Masareef.amount.like('%{}%'.format(search)),
        Masareef.date.like('%{}%'.format(search))
    ))
    return render_template('masrf.html', query=filte, form=form)