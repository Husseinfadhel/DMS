from flask import Flask, render_template, request, flash, url_for, redirect
from models import setup_db, Client, Driver, Masareef, Orders, Users
from forms import AddClient, Search, AddDriver, AddMasrf, AddOrder
from datetime import datetime
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

        elif user == record.username and password == record.password and record.drive is None and record.entry is None:
            return redirect(url_for('main'))
        elif user == record.username and password == record.password and record.entry == 0 and record.drive is None:
            return redirect(url_for("add_order"))
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
        phone=request.form['phone'],
        shop=request.form['shop']
    )
    Client.insert(new)
    flash('???????????? ' + request.form['name'] + ' ???? ???????????? ??????????')
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

@app.route('/kashf', methods=["GET", "POST"])
def kashf():
    num = 0
    net = 0
    record_id = request.form['py']
    query = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                            Driver.id == Orders.driver_id, Orders.client_id == record_id, Orders.state != 0, Orders.payment_state == 0).all()
    for o,s,c in query:
        if o.state == 1:
            num += o.total_cost
            net += o.net_cost

    return render_template('kshf.html', query=query, num=num, net=net)

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
    num = 0
    for ll in query:
        num += ll.amount
    return render_template('masrf.html', query=query, form=form, num=num)


@app.route('/masrf', methods=['POST'])
def masrf_post():
    search = request.form['search']
    form = Search()
    h1 = request.form['h1']
    h2 = request.form['h2']
    if len(h1) > 1 and len(h2) > 1:

        filte = Masareef.query.filter(db.or_(
            Masareef.reason.like('%{}%'.format(search)),
            Masareef.amount.like('%{}%'.format(search)),
            Masareef.date.like('%{}%'.format(search))), db.and_(Masareef.date >= h1, Masareef.date <= h2)
        )
        num = 0
        for ll in filte:
            num += ll.amount
        return render_template('masrf.html', query=filte, form=form, num=num)
    else:
        filte = Masareef.query.filter(db.or_(
            Masareef.reason.like('%{}%'.format(search)),
            Masareef.amount.like('%{}%'.format(search)),
            Masareef.date.like('%{}%'.format(search))
        ))
        num = 0
        for ll in filte:
            num += ll.amount
        return render_template('masrf.html', query=filte, form=form, num=num)


@app.route('/add/order', methods=['GET'])
def add_order():
    order = AddOrder()
    clients = Client.query.all()
    drivers = Driver.query.all()
    return render_template('addorder.html', form=order, clients=clients, drivers=drivers)


@app.route('/add/order', methods=['POST'])
def add_order_post():
    record = Client.query.filter_by(shop=request.form['client']).first()

    h = request.form['date']
    note = request.form['note']
    new = Orders(invoice_num=request.form['invoice_num'],
                 client_id=record.id,
                 total_cost=request.form['total'],
                 net_cost=request.form['net'],
                 driver_id=request.form['driver'],
                 date=h,
                 costumer=request.form['costumer'],
                 costumer_add=request.form['costumer_add'],
                 costumer_phone=request.form['costumer_phone'],
                 notes=note
                 )
    Orders.insert(new)
    return redirect(url_for('add_order'))


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
    today=datetime.today().strftime('%Y-%m-%d')
    query = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                            Driver.id == Orders.driver_id, Orders.date == today )
    form = Search()
    num = 0
    net = 0

    for to, t, z in query:
        if to.state == 1 and to.payment_state == 0:
            num += to.total_cost
            net += to.net_cost
    return render_template('order.html', query=query, form=form, num=num, net=net)


@app.route('/order', methods=['POST'])
def order_post():
    search = request.form['search']
    h1 = str(request.form['h1'])
    h2 = str(request.form['h2'])
    form = Search()
    if len(request.form['h1']) > 1 and len(request.form['h2']) > 1:
        # h1 = h1.split('-')
        # h2 = h2.split('-')
        # h1 = date(year=int(h1[0]), month=int(h1[1]), day=int(h1[2]))
        # h2 = date(year=int(h2[0]), month=int(h2[1]), day=int(h2[2]))

        filte = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                                Driver.id == Orders.driver_id, db.or_(
                Orders.invoice_num.like('%{}%'.format(search)), Client.shop.like('%{}%'.format(search)),
                Driver.name.like('%{}%'.format(search))), db.and_(
                Orders.date >= h1, Orders.date <= h2))

        num = 0
        net = 0
        for to, t, z in filte:
            if to.state == 1 and to.payment_state == 0:
                num += to.total_cost
                net += to.net_cost
        return render_template('order.html', query=filte, form=form, num=num, net=net)
    else:
        filte = db.session.query(Orders, Driver, Client).filter(Client.id == Orders.client_id,
                                                                Driver.id == Orders.driver_id,
                                                                Orders.payment_state == 0, db.or_(
                Orders.invoice_num.like('%{}%'.format(search)), Client.shop.like('%{}%'.format(search)),
                Driver.name.like('%{}%'.format(search))
            ))
        num = 0
        net = 0
        for to, t, z in filte:
            if to.state == 1 and to.payment_state == 0:
                num += to.total_cost
                net += to.net_cost
        return render_template('order.html', query=filte, form=form, num=num, net=net)

    return redirect(url_for('order'))


@app.route('/edit-order', methods=['POST'])
def edit_order():
    orde = request.form['order']
    query = Orders.query.get(orde)
    client = Client.query.get(query.client_id)
    drivers = Driver.query.all()
    return render_template('editorder.html', query=query, drivers=drivers, client=client)


@app.route('/edit', methods=['POST'])
def edit():
    orde = request.form['id']
    query = Orders.query.get(orde)
    client = Client.query.filter(Client.shop == request.form['shop']).first()
    query.client_id = client.id
    query.invoice_num = request.form['invoice_num']
    query.costumer = request.form['costumer']
    query.costumer_phone = request.form['costumer_phone']
    query.costumer_add = request.form['costumer_add']
    query.date = request.form['date']
    query.total_cost = request.form['total']
    query.net_cost = request.form['net']
    query.driver_id = request.form['driver']
    query.notes = request.form['note']
    Orders.update(query)

    return redirect(url_for('order'))


@app.route('/state', methods=['POST'])
def state():
    change = Orders.query.get(request.form['order'])
    change.state = request.form['state']
    Orders.update(change)
    return redirect(url_for("order"))


@app.route('/payment', methods=['POST'])
def payment():
    change = Orders.query.filter(Orders.client_id == request.form['py'])
    for record in change:
        if record.state == 1 or record.state == 2:
            record.payment_state = 1
            Orders.update(record)
    return redirect(url_for("client"))


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


@app.route("/delete-order", methods=["POST"])
def delete_order():
    order = Orders.query.get(request.form['order'])
    Orders.delete(order)
    return redirect(url_for("order"))


@app.route("/delete-masrf", methods=["POST"])
def delete_masrf():
    masrf = Masareef.query.get(request.form['masrf'])
    Masareef.delete(masrf)
    return redirect(url_for("masrf"))


@app.route("/delete-driver", methods=["POST"])
def delete_driver():
    driv = Driver.query.get(request.form['driver'])
    Driver.delete(driv)
    return redirect(url_for('driver'))


@app.route("/delete-client", methods=["POST"])
def delete_client():
    cli = Client.query.get(request.form['client'])
    Client.delete(cli)

    return redirect(url_for("client"))


if __name__ == "__main__":
    app.run(debug=False)
