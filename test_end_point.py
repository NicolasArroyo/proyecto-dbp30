from urllib import response
from app import app, url_for, request, abort
import unittest

try:
    from app import app
    import unittest

except Exception as e:
    print("Some Modules are Missing {}". format(e))


class Flask_Test(unittest.TestCase):

    #Check for response 200
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        statuscode = response.status_code
        self.assertEquals(statuscode, 200)
    
    #check if content retur is text/html
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/register/newUser")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    """#check for Data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/register/newUser")
        self.assertTrue(b'Message' in response.data)"""


    def test_endpoint_home(self):
        tester = app.test_client(self)
        response = tester.get("/register")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")
    
    def test_endpoint_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        assert response.request.path == "/"
        

"""    def test_endpoint_register(self):
        tester = app.test_client(self)
        response = tester.get("/register")
    def test_endpoint_register_newUser(self):
        tester = app.test_client(self)
        response = tester.get("/register")
    def test_endpoint_login(self):
        tester = app.test_client(self)
        response = tester.get("/register")
    def test_endpoint_logout(self):
        tester = app.test_client(self)
        response = tester.get("/register")
    def test_endpoint_settings(self):
        tester = app.test_client(self)
        response = tester.get("/register")
    def test_endpoint_settings_newPassword(self):
        tester = app.test_client(self)
        response = tester.get("/register")
    def test_endpoint_settings_deleteUser(self):
        tester = app.test_client(self)
        response = tester.get("/register")"""
"""
class TestErrorPages(TestBase):

	def test_403_forbidden(self):
		# create route to abort the request with the 403 Error
		@self.errorhandler(403)
		def forbidden_error():
			abort(403)

		response = self.client.get('/403')
		self.assertEqual(response.status_code, 403)
		self.assertTrue("403 Error" in response.data)

	def test_404_not_found(self):
		response = self.client.get('/nothinghere')
		self.assertEqual(response.status_code, 404)
		self.assertTrue("404 Error" in response.data)

	def test_500_internal_server_error(self):
		# create route to abort the request with the 500 Error
		@self.errorhandler(500)
		def internal_server_error():
			abort(500)

		response = self.client.get(500)
		self.assertEqual(response.status_code, 500)
		self.assertTrue("500 Error" in response.data)"""

if __name__ == "__main__":
    unittest.main()
