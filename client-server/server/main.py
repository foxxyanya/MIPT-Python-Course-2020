import flask
import lib
import json


client_list = lib.ClientList()
order = lib.Order()


app = flask.Flask('bakery-server')


@app.route('/logIn', methods=['POST'])
def log_in():
    login = flask.request.json['login']
    order.log_in(login)
    client_list.verify_user(login)
    return 'OK'


@app.route('/getCashe', methods=['GET'])
def get_cashe():
    return str(client_list.get_cashe(order.get_login()))


@app.route('/getInStock', methods=['GET'])
def get_bakes():
    type = flask.request.json['type']
    return json.dumps(order.bake_in_stock[type])


@app.route('/put', methods=['POST'])
def put():
    args = flask.request.json
    type = args['type']
    filling = args['filling']
    size = args['size']
    order.put_in_basket(type, filling, size)
    return 'OK'


@app.route('/getAllTypes', methods=['GET'])
def get_types():
    return json.dumps(order.poss_arguments['type'])


@app.route('/getAllArguments', methods=['GET'])
def get_param():
    return json.dumps(order.poss_arguments)


@app.route('/getTotal', methods=['GET'])
def total_sum():
    return str(order.total)


@app.route('/getBasket', methods=['GET'])
def get_basket():
    return json.dumps(order.get_basket())


@app.route('/isLoggedIn', methods=['GET'])
def is_logged_in():
    if order.logged_in():
        return 'YES'
    return 'NO'


@app.route('/pay', methods=['POST'])
def pay():
    client_list.change_cashe(order.login, order.total)
    order.log_out()
    return 'OK'


@app.route('/leave', methods=['POST'])
def leave():
    order.log_out()
    return 'OK'


def main():
    port = input('Enter port>')
    app.run('::', port=port)


if __name__ == '__main__':
    main()
