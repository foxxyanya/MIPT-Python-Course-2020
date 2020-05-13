import unittest
import lib


class TestOrder(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = lib.Order()
        self.order.logIn('fox')
        self.order.putInBasket('cupcake', 'cream', 'big')
    def test_login(self):
        self.assertTrue(self.order.loggedIn())
    def test_putting_in_basket(self):
        self.assertNotEqual(self.order.getTotal(), 0)
    def test_cleaning_basket(self):
        self.order.logOut()
        self.order.logIn('fox')
        self.assertEqual(len(self.order.getBasket()), 0)
    def tearDown(self):
        self.order.logOut()


class TestClientList(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_list = lib.ClientList()
        self.client_list.verifyUser('fox')
        self.client_list.verifyUser('cat')
    def test_verifying(self):
        self.assertIn('fox', self.client_list.clients)
    def test_verifying2(self):
        with self.assertRaises(ValueError):
            self.client_list.changeCashe('dog', 5)
    def tearDown(self):
        self.client_list.clean()




