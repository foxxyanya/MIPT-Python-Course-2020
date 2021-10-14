import requests
import argparse
import json


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8000


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=DEFAULT_HOST)
    parser.add_argument('--port', default=DEFAULT_PORT, type=int)
    return parser


def correct_input(correct, message='Enter'):
    while True:
        item = input(f'{message}>')
        if not item in correct:
            print('Incorrect input, try again')
        else:
            return item


def ask_to_choose(list_, message='Choose', pointer='-'):
    print(f'{message}:')
    for item in list_:
        print(pointer, item)


def url(args):
    return f'http://{args.host}:{args.port}'


def choose(url):
    types = json.loads(requests.get(f'{url}/getAllTypes').text)
    ask_to_choose(types)
    type = correct_input(types, 'Which one?')
    options = json.loads(requests.get(f'{url}/getInStock', json={'type': type}).text)
    print(f'We have next variants of {type}:')
    correct = []
    for i, opt in enumerate(options):
        print(i, '-', type, opt)
        correct.append(str(i))
    correct.append('None')
    num = correct_input(correct, 'Enter number or "None"')
    if num != 'None':
        parameter = options[int(num)].split()
        requests.post(f'{url}/put', json={'type': type, 'filling': parameter[0], 'size': parameter[1]})
        print('It\'s in your basket now')
    else:
        print('Enter "create" to make your own bake!')


def create(url):
    args = json.loads(requests.get(f'{url}/getAllArguments').text)
    types = args['type']
    fillings = args['filling']
    sizes = args['size']
    ask_to_choose(types, 'Choose any type')
    type = correct_input(types, 'type')
    ask_to_choose(fillings, 'Choose any filling')
    filling = correct_input(fillings, 'filling')
    ask_to_choose(sizes, 'Choose any size')
    size = correct_input(sizes, 'size')
    requests.post(f'{url}/put', json={'type': type, 'filling': filling, 'size': size})
    print('It\'s in your basket now')


def sum(url):
    sum = requests.get(f'{url}/getTotal').text
    print('Current cost of your order is', sum, '$')


def exit_(url):
    requests.post(f'{url}/leave')
    print(' See you soon!')
    exit()


def basket(url):
    bask = json.loads(requests.get(f'{url}/getBasket').text)
    for bake in bask:
        print('-', end=' ')
        for par in bake:
            print(par, end=' ')
        print()


def help():
    print('cashback', '-', 'Show cashback from previous orders')
    print('choose', '-', 'Choose bake from stock')
    print('create', '-', 'Create a bake with your parameters')
    print('sum', '-', 'Show total order\'s sum')
    print('pay', '-', 'Pay and logOut')
    print('basket', '-', 'Show bakes you\'ve ordered')
    print('help', '-', 'Get some help')
    print('exit', '-', 'Logout and exit')


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()
    url_ = url(main_args)
    while True:
        isLoggedIn = requests.get(f'{url_}/isLoggedIn').text
        if isLoggedIn == 'NO':
            login = input('Please, enter your login>')
            requests.post(f'{url_}/logIn', json={'login': login})
            print('Welcome!')
        try:
            cmd = input('Enter command>')
            if cmd == 'choose':
                choose(url_)
            elif cmd == 'create':
                create(url_)
            elif cmd == 'cashback':
                cashe = requests.get(f'{url_}/getCashe').text
                print('Your cashback is', cashe, '$')
            elif cmd == 'sum':
                sum(url_)
            elif cmd == 'pay':
                requests.post(f'{url_}/pay')
                print('See you soon!')
            elif cmd == 'basket':
                basket(url_)
            elif cmd == 'help':
                help()
            elif cmd == 'exit':
                exit_(url_)
            else:
                print('Unknown command')
        except KeyboardInterrupt:
            exit_(url_)


if __name__=='__main__':
    main()
