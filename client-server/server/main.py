import flask
import lib


client_list = lib.ClientList()
order = lib.Order()


app = flask.Flask('bakery-server')


@app.route('/logIn', methods=['POST'])
def log_in():
    login = str(flask.request.args['login'])
    order.logIn(login)
    client_list.verifyUser(login)
    return 'OK'

@app.route('/getCashe', methods=['GET'])
def get_cashe():
    return str(client_list.getCashe(order.getLogin()))



@app.route('/getInStock', methods=['GET'])
def get_bakes():
    type = str(flask.request.args['type'])
    poss_var = order.bake_in_stock[type]
    s = str()
    for el in poss_var:
        s += el + '&'
    return s



@app.route('/put', methods=['POST'])
def put():
    req_args = flask.request.args
    type = req_args['type']
    filling = req_args['filling']
    size = req_args['size']
    order.putInBasket(type, filling, size)
    return 'OK'


@app.route('/getAllTypes', methods=['GET'])
def get_types():
    s = str()
    for type in order.poss_arguments['type']:
        s += type + '&'
    return s


@app.route('/getAllArguments', methods=['GET'])
def get_param():
    s = str()
    for param, args in order.poss_arguments.items():
        for arg in args:
            s += arg + ' '
        s += '&'
    return s


@app.route('/getTotal', methods=['GET'])
def total_sum():
    return str(order.total)


@app.route('/getBasket', methods=['GET'])
def get_basket():
    s = str()
    for bake in order.getBasket():
        for par in bake:
            s += par + ' '
        s += '&'
    return s


@app.route('/isLoggedIn', methods=['GET'])
def is_logged_in():
    if order.loggedIn():
        return 'YES'
    return 'NO'


@app.route('/pay', methods=['POST'])
def pay():
    client_list.changeCashe(order.login, order.total)
    order.logOut()
    return 'OK'


@app.route('/leave', methods=['POST'])
def leave():
    order.logOut()
    return 'OK'


def main():
    app.run('::', port=8000)


if __name__ == '__main__':
    main()