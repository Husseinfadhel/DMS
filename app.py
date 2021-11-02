from flask import Flask, render_template, request, flash, url_for, redirect, session
from models import setup_db, Client, Driver, Masareef, Orders, Users
from forms import AddClient, Search, AddDriver, AddMasrf, AddOrder

app = Flask(__name__, template_folder='templates')

db = setup_db(app)


@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/', methods=['POST'])
def login_post():
    user = str(request.form['user'])
    password = int(request.form['pass'])
    query = Users.query.all()
    for record in query:
        if user == record.username and password == record.password and record.drive is not None:
            driv = record.drive
            return redirect(url_for("orderdr", driv=driv))

        elif user == record.username and password == record.password and record.drive is None:
            print(record.drive)
            return redirect(url_for('main'))
    return redirect(url_for('login'))


@app.route('/order/<int:driv>', methods=['GET', "POST"])
def orderdr(driv):
    if request.method == "GET":
        query = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                                Orders.driver_id == Driver.id,
                                                                Driver.id == driv
                                                                ).all()
        form = Search()
        return render_template('orderdr.html', query=query, form=form)

    elif request.method == "POST":
        search = request.form['search']
        form = Search()
        filte = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                                Driver.id == Orders.driver_id, Driver.id == driv,
                                                                db.or_(
                                                                    Orders.invoice_num.like('%{}%'.format(search)),
                                                                    Client.name.like('%{}%'.format(search))
                                                                ))
        return render_template('orderdr.html', query=filte, form=form)


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


@app.route('/add/order', methods=['GET'])
def add_order():
    order = AddOrder()
    clients = Client.query.all()
    drivers = Driver.query.all()
    return render_template('addorder.html', form=order, clients=clients, drivers=drivers)


@app.route('/add/order', methods=['POST'])
def add_order_post():
    record = Client.query.filter_by(name=request.form['client']).first()
    new = Orders(invoice_num=request.form['invoice_num'],
                 client_id=record.id,
                 total_cost=request.form['total'],
                 net_cost=request.form['net'],
                 driver_id=request.form['driver'],
                 date=request.form['date']
                 )
    Orders.insert(new)
    return redirect(url_for('main'))


@app.route('/add/account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'GET':
        drivers = Driver.query.all()
        return render_template("account.html", drivers=drivers)
    elif request.method == 'POST':
        drivor = int(request.form['driver'])
        user = request.form['user']
        password = int(request.form['pass'])
        new = Users(username=user,
                    password=password,
                    drive=drivor)
        Users.insert(new)
        return redirect(url_for('main'))


@app.route('/order', methods=['GET'])
def order():
    query = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                            Driver.id == Orders.driver_id).all()
    form = Search()
    return render_template('order.html', query=query, form=form)


@app.route('/order', methods=['POST'])
def order_post():
    search = request.form['search']
    form = Search()
    filte = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                            Driver.id == Orders.driver_id, db.or_(
            Orders.invoice_num.like('%{}%'.format(search)), Client.name.like('%{}%'.format(search))
        ))
    return render_template('order.html', query=filte, form=form)


@app.route('/state', methods=['POST'])
def state():
    change = Orders.query.get(request.form['order'])
    change.state = request.form['state']
    Orders.update(change)
    return redirect(url_for("order"))


@app.route('/state2', methods=['POST'])
def state2():
    change = Orders.query.get(request.form['order'])
    change.state = request.form['state']

    Orders.update(change)
    driver_id = request.form['driver']
    query = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                            Orders.driver_id == driver_id
                                                            ).all()
    form = Search()

    return render_template('orderdr.html', query=query, form=form)


if __name__ == "__main__":
    app.run(debug=True)
