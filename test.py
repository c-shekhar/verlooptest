import json
import unittest
from web import server

class TestCases(unittest.TestCase):
	def setUp(self):
		server.app.config['TESTING'] = True
		self.app = server.app.test_client()

	#test for valid organization-id
	def test_valid_organization_repos(self):
		response = self.app.post("/repos",json={'org':'verloop'})
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(data['results']), 3)

	#test for invalid organization-id
	def test_invalid_organization_repos(self):
		response = self.app.post("/repos",json={'org':'xxx'})
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(data['results'], [])
		self.assertEqual(data['error'], 'HTTP error')

	#test for invalid request with a GET request
	def test_invalid_get_request(self):
		response = self.app.get("/repos",data={'org':'verloop'})
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(data['results'], [])
		self.assertEqual(data['error'], "Invalid Request. Check if you are making a POST request.")

	#test for invalid request without payload
	def test_invalid_request_with_incorrect_headers(self):
		response = self.app.post("/repos")
		data = json.loads(response.get_data(as_text=True))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(data['results'], [])
		self.assertEqual(data['error'], "Invalid Request. Check request payload or content-type.")

if __name__ == '__main__':
	unittest.main()