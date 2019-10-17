from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

# Example item
pineapple_id = ObjectId('5da00f106c1c3b4daf43e0ad')
pineapple = {
    'title': 'pineapple',
    'price': '$1',
    'img': [
        '/static/images/pineapple.jpg'
    ]
}
sample_form_data = {
    'title': pineapple['title'],
    'price': pineapple['price'],
    'img': '\n'.join(pineapple['img'])
}

class ContractorTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    # makes sure the '/'(homepage) is running well
    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    # makes sure the '/new' page is running well
    def test_cart(self):
        result = self.client.get('/products/new')
        self.assertEqual(result.status, '200 OK')

    # makes sure that the code understands that the title of the the sock is pineapple
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_pineapple(self, mock_find):
        mock_find.return_value = pineapple
        result = self.client.get(f'/products/{pineapple_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'pineapple', result.data)

if __name__ == '__main__':
    unittest_main()