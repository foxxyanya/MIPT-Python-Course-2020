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
    def loggedIn(self):
        return self.opened
    def logIn(self, user):
        self.login = user
        self.opened = True
    def getLogin(self):
        return self.login
    def getTotal(self):
        return self.total
    def putInBasket(self, type, fill, size):
        bake = Bake(type, fill, size)
        self.basket.append(bake)
        self.total += bake.price()
    def getBasket(self):
        basket = list()
        for bake in self.basket:
            l = list()
            l.append(bake.type)
            l.append(bake.filling)
            l.append(bake.size)
            basket.append(l)
        return basket
    def logOut(self):
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
    def verifyUser(self, user):
        if not user in self.clients:
            self.clients.append(user)
            self.cashe.append(0)
    def getCashe(self, user):
        cashe = self.cashe[self.clients.index(user)]
        return ('%.2f' % cashe)
    def changeCashe(self, user, sum):
        self.cashe[self.clients.index(user)] = sum * self.CASHE
    def clean(self):
        self.clients = []
        self.cashe = []
