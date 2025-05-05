import unittest
import json
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
    
    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_calculate_route_success(self):
        response = self.client.post('/calculate', 
                                   data=json.dumps({'expression': '2 + 3'}),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 5)
    
    def test_calculate_route_error(self):
        response = self.client.post('/calculate', 
                                   data=json.dumps({'expression': '2 /'}),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
    
    def test_complex_calculation(self):
        response = self.client.post('/calculate', 
                                   data=json.dumps({'expression': '(2 + 3) * sqrt(16)'}),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 20)
    
    def test_missing_expression(self):
        response = self.client.post('/calculate', 
                                   data=json.dumps({}),
                                   content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['result'], 0)  # Empty expression returns 0

if __name__ == '__main__':
    unittest.main()