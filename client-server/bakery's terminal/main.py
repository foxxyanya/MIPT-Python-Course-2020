import requests
import argparse


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default = 'localhost')
    parser.add_argument('--port', default=8000, type=int)
    return parser


def correct_input(correct, message='Enter'):
    while True:
        item = input(f'{message}>')
        if not item in correct:
            print('Incorrect input, try again')
        else:
            return item

def ask_to_choose(list_, message='Choose',pointer='-'):
    print(f'{message}:')
    for item in list_:
        print(pointer, item)


def split(s):
    l = s.split('&')
    if '' in l:
        l.remove('')
    return l


def url(args):
    return f'http://{args.host}:{args.port}'


def choose(main_args):
    types = split(requests.get(f'{url(main_args)}/getAllTypes').text)
    ask_to_choose(types)
    bake = correct_input(types, 'Which one?')
    options = split(requests.get(f'{url(main_args)}/getInStock?type={bake}').text)
    print(f'We have next variants of {bake}:')
    correct = []
    for i, opt in enumerate(options):
        print(i, '-', bake, opt)
        correct.append(str(i))
    correct.append('None')
    num = correct_input(correct, 'Enter number or "None"')
    if num != 'None':
        parametr = options[int(num)].split()
        requests.post(
            f'{url(main_args)}/put?type={bake}&filling={parametr[0]}&size={parametr[1]}')
        print('It\'s in your basket now')
    else:
        print('Enter "create" to make your own bake!')


def create(main_args):
    args = split(requests.get(f'{url(main_args)}/getAllArguments').text)
    types = args[0].split()
    fillings = args[1].split()
    sizes = args[2].split()
    ask_to_choose(types, 'Choose any type')
    type = correct_input(types, 'type>')
    ask_to_choose(fillings, 'Choose any filling')
    filling = correct_input(fillings, 'filling>')
    ask_to_choose(sizes, 'Choose any size')
    size = correct_input(sizes, 'size>')
    requests.post(f'{url(main_args)}/put?type={type}&filling={filling}&size={size}')
    print('It\'s in your basket now')


def sum(main_args):
    sum = requests.get(f'{url(main_args)}/getTotal').text
    if sum == 'fail':
        print('Please, logIn!')
    else:
        print('Current cost of your order is', sum, '$')


def help():
    print('cashback', '-', 'Show cashback from previous orders')
    print('choose', '-', 'Choose bake from stock')
    print('create', '-', 'Create a bake with your parameters')
    print('sum', '-', 'Show total order\'s sum')
    print('pay', '-', 'Pay and logOut')
    print('basket', '-', 'Show bakes you\'ve ordered')
    print('help', '-', 'Get some help')


def main():
    main_parser = create_main_parser()
    main_args = main_parser.parse_args()
    while True:
        isLoggedIn = requests.get(f'{url(main_args)}/isLoggedIn').text
        if isLoggedIn == 'NO':
            login = input('Please, enter your login>')
            requests.post(f'{url(main_args)}/logIn?login={login}').text
            print('Welcome!')
        try:
            cmd = input('Enter command>')
            if cmd == 'choose':
                choose(main_args)
            elif cmd == 'create':
                create(main_args)
            elif cmd == 'cashback':
                cashe = requests.get(f'{url(main_args)}/getCashe').text
                print('Your cashback is', cashe, '$')
            elif cmd == 'sum':
                sum(main_args)
            elif cmd == 'pay':
                requests.post(f'{url(main_args)}/pay')
                print('See you soon!')
            elif cmd == 'basket':
                basket = split(requests.get(f'{url(main_args)}/getBasket').text)
                for bake in basket:
                    print('-', bake)
            elif cmd == 'help':
                help()
            else:
                print('Unknown command')
        except KeyboardInterrupt:
            requests.post(f'{url(main_args)}/leave')
            print(' See you soon!')
            exit()


if __name__=='__main__':
    main()