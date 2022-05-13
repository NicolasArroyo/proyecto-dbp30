
from pickle import TRUE
from app import Account

def test_new_account():
    account = Account('Matias Jose', 'Castro Mendoza', 'matias_mjcm', '995712594', '2', TRUE, 'matias.castro@utec.edu.pe')
    assert account.first_name == 'Matias Jose'
    assert account.last_name == 'Castro Mendoza'
    assert account.password == '995712'