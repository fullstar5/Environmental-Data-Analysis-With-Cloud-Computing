import unittest, requests, json, time

class HTTPSession:
    def __init__(self, protocol, hostname, port):
        self.session = requests.session()
        self.base_url = f'{protocol}://{hostname}:{port}'

    def get(self, path):
        return self.session.get(f'{self.base_url}{path}')

class TestEnd2End(unittest.TestCase):

    def test_bom(self):
        r= test_request.get('/bom?size=1')
        self.assertEqual(r.status_code, 200)
        o= r.json()[0]['_source']
        self.assertEqual(o['site_name'], 'Melbourne (Olympic Park)')

        r= test_request.get('/bom?start=6&weather=good')
        self.assertEqual(r.status_code, 200)
        o= r.json()
        self.assertEqual(len(o), 0)

        self.assertEqual(test_request.get('/bom?start=2').status_code, 500)

    def test_epa(self):
        r= test_request.get('/epa?size=2')
        self.assertEqual(r.status_code, 200)
        o= r.json()[1]['_source']
        self.assertEqual(o['healthParameter'], 'PM2.5')

    def test_health(self):
        r= test_request.get('/health?size=3')
        o= r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(o), 3)
        self.assertEqual(o[2]['_source']['SR'], 129)

    def test_twitter(self):
        r= test_request.get('/twitter?size=1')
        o= r.json()[0]['_source']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(o['sentiment'], 0.1)

if __name__ == '__main__':

    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()
