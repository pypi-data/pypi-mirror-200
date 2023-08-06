import os

__envvars = [
    'PHOTO_BURST_DETECTION_PATH',
    'SECRET_KEY',
    'LDAP_HOST',
    'LDAP_PORT',
    'LDAP_BASE_DN',
    'LDAP_USER_DN',
    'LDAP_GROUP_DN',
    'LDAP_USER_RDN_ATTR',
    'LDAP_USER_LOGIN_ATTR',
    'LDAP_BIND_USER_DN',
    'LDAP_BIND_USER_PASSWORD',
    'LDAP_GROUP_OBJECT_FILTER',
]

config = {'SECRET_KEY': 'secret'}

if 'PHOTO_BURST_DETECTION_CONFIG' in os.environ:
    with open(os.environ['PHOTO_BURST_DETECTION_CONFIG'], 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            try:
                key, value = line.strip().split('=', 1)
                config[key] = value
            except Exception as e:
                print(f'error : {e} on {line}')

for var in __envvars:
    if var in os.environ:
        config[var] = os.environ[var]


print('#####################')
print('### configuration ###')
for k, v in config.items():
    print(f'{k}={v}')
print('#####################')
