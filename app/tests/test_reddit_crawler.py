import unittest
from app import rest_api as api

class API_Routes_TestCase(unittest.TestCase):

	def setUp(self):
		api.app.config['DEBUG'] = True
		api.app.config['TESTING'] = True
		self.app = api.app.test_client(self)

	def test_get_users_missing_param(self):
		response = self.app.get('/api/users')
		self.assertEqual('{"status": "400", "message": "Parameter required: order_by"}', response.data)

	def test_get_users_invalid_param(self):
		response = self.app.get('/api/users?order_by=dsdd')
		self.assertEqual('{"status": "400", "message": "Invalid value for parameter: order_by. Valid values: num_comments, num_submissions, value"}', response.data)

	def test_get_user_submissions_invalid_param(self):
		response = self.app.get('/api/submissions?order_by=-32')
		self.assertEqual('{"status": "400", "message": "Invalid value for parameter: order_by. Valid values: num_comments, punctuation"}', response.data)

if __name__ == '__main__':
	unittest.main()
