from hashlib import md5
from urllib.parse import urlencode

from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, UserMixin

from photo_burst_detection import app

login_manager = LoginManager(app)
ldap_manager = LDAP3LoginManager(app)

users = {}


class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data
        if len(data['mail']) > 0:
            self.email = data['mail'][0].lower().strip()
            email_hash = md5(self.email.encode()).hexdigest()
            params = urlencode({'d': 'retro', 's': '40'})
            self.gravatar_url = f'https://www.gravatar.com/avatar/{email_hash}?{params}'

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn


@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None


@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user
