class Order:
    poss_parametrs = ['type', 'filling', 'size']
    poss_arguments = {'type' : ['donut', 'croissant', 'cupcake'],
                      'filling' : ['cream', 'chocolate', 'jam'],
                      'size' : ['small', 'big']}
    bake_in_stock = {'donut': ['cream small', 'jam small'],
                     'croissant': ['chocolate big'],
                     'cupcake': ['cream big']}
    def __init__(self,):
        self.login = ''
        self.opened = False
        self.basket = []
        self.total = 0
    def logged_in(self):
        return self.opened
    def log_in(self, user):
        self.login = user
        self.opened = True
    def get_login(self):
        return self.login
    def get_total(self):
        return self.total
    def put_in_basket(self, type, fill, size):
        bake = Bake(type, fill, size)
        self.basket.append(bake)
        self.total += bake.price()
    def get_basket(self):
        basket = list()
        for bake in self.basket:
            l = list()
            l.append(bake.type)
            l.append(bake.filling)
            l.append(bake.size)
            basket.append(l)
        return basket
    def log_out(self):
        self.opened = False
        self.basket = []
        self.total = 0


class Bake:
    price_for_small = 3.5
    price_for_big = 6.0
    def __init__(self, type, fill, size):
        self.type = type
        self.filling = fill
        self.size = size
    def price(self):
        return self.price_for_small if self.size == 'small' \
                else self.price_for_big



class ClientList:
    CASHE = 0.2
    def __init__(self):
        self.clients = []
        self.cashe = []
    def clients(self):
        return self.clients
    def verify_user(self, user):
        if not user in self.clients:
            self.clients.append(user)
            self.cashe.append(0)
    def get_cashe(self, user):
        cashe = self.cashe[self.clients.index(user)]
        return ('%.2f' % cashe)
    def change_cashe(self, user, sum):
        self.cashe[self.clients.index(user)] = sum * self.CASHE
    def clean(self):
        self.clients = []
        self.cashe = []
