from pickle import TRUE
import pytest
from app import Account



def test_new_user():
    account = Account('matias', 'castro', 'matiasmjcm', '995712594', 0, TRUE, 'matias_castro@hotmail.com')
    account = Account('juan', 'alvarado', 'juanalv', '12345', 0, TRUE, 'juan_alvarado@hotmail.com')
    assert account.first_name == 'matias'
    assert account.last_name == 'mendoza'
    assert account.email == 'juan_alvarado@hotmail.com'
    assert account.password == '12345'


