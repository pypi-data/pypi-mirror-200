from lementpro.data.user import User
from lementpro.services.accounts import Accounts


def test_login():
    Accounts().login(login="sss", password="ddd", by_user=User(root_url="https://ugate.dev.lement.ru"))
