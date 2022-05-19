from urllib import response
from app import app
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
        response = tester.get("/register/newUser")
        statuscode = response.status_code
        self.assertEquals(statuscode, 200)
    
    #check if content retur is application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/register/newUser")
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    #check for Data returned
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/register/newUser")
        self.assertTrue(b'Message' in response.data)

if __name__ == "__main__":
    unittest.main()
