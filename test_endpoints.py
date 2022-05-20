import email
from pickle import FALSE, TRUE
from urllib import response
from app import (app, url_for, request, abort, Account, 
                Book, Author, FlaskForm, StringField, 
                PasswordField, SubmitField, InputRequired, 
                Length, ValidationError, Bcrypt)
import unittest, pytest

try:
    from app import app, url_for, request, abort, Account, Book, Author
    import unittest
except Exception as e:
    print("Some Modules are Missing {}".format(e))

def test_Account_Model():
    account = Account('matias', 'castro', 'matiasmjcm', '995712594', 0, TRUE, 'matias_castro@hotmail.com', FALSE)
    assert account.first_name == 'matias';
    assert account.last_name == 'castro';
    assert account.is_admin == FALSE;
def test_Book_Model():
    book = Book('AJ123', 'El Capo', 'Gleen Black', 'Español', 125, 2002-12-12, 'Cosmo Editores', 75, 1872-12-12, 1971-12-12)
    assert book.ISBN == 'AJ123'
    assert book.language == 'Español'
    assert book.publication_date == 2002-12-12
def test_Author_Moder():
    author = Author('Gleen Black', 1988-12-12)
    assert author.name == 'Gleen Black'
    assert author.dob == 1988-12-12


 

class Flask_Tets_Routes(unittest.TestCase):
    #Test redirect tu home.html (success == 200)
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        assert response.status_code == 200
    
    def test_home_serch(self):
        tester = app.test_client(self)
        response = tester.get("/home/search")
        assert response.status_code == 200
        self.assertEqual(response.content_type, "application/json")
    
    def test_home_rent(self):
        tester = app.test_client(self)
        response = tester.post("/home/rent")
        assert response.status_code == 200
        self.assertEqual(response.content_type, "application/json")
    
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        assert response.status_code == 302

    def test_register(self):
        tester = app.test_client(self)
        response = tester.post('/register', 
                                data = dict(firstname = 'Juan', lastName = 'Alvarado',
                                            username = 'juan_alvarado', password = '123456',
                                            email = 'matias_mjcm@hotmail.com'),
                                follow_redirects=True)
        assert response.status_code == 200

        response = tester.get('/logout', follow_redirects=True)
        assert response.status_code == 200

        print("Correct registration HTTP-code: " + str(response.status_code))
        
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data

    def test_settings_newPassword(self):
        tester = app.test_client(self)
        response = tester.post('/settings/newPassword')
        assert response.status_code == 302




    """
    Se implementara mas adelante, ya que se desea una mayor interaccion cone estos endpoints
    def test_settings_deleteUser():
    def test_addBook():
    def test_addBook_new():
    def test_addAuthor():
    def test_addAuthor_new():"""

if __name__ == "__main__":
    unittest.main()