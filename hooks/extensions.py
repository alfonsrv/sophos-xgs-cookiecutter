import secrets
import string

from cookiecutter.utils import simple_filter


@simple_filter
def domain_component(value):
    """ Makes an LDAP compatible Domain Component query (rausys.loc ==> DC=rausys,DC=loc) """
    components = value.split('.')
    formatted = ''
    for component in components:
        formatted += f'DC={component},'
    return formatted[:-1]


@simple_filter
def netbios(value):
    return value.split('.')[:1][0]


@simple_filter
def dhcp_lease(value):
    # 10.20.5.150-10.20.5.151
    ip_addr_start = '.'.join(value.split('.')[:-1]+["10"])
    ip_addr_end = '.'.join(value.split('.')[:-1]+["225"])
    return f'{ip_addr_start}-{ip_addr_end}'


@simple_filter
def scope_translate(value):
    return '.'.join(value.split('.')[:-1])


@simple_filter
def strong_password(value):
    LENGTH = 64
    alphabet = string.ascii_letters + string.digits + '.,&!?_' + string.ascii_letters
    password = ''.join(secrets.choice(alphabet) for _ in range(LENGTH))
    password = '-'.join([password[i:i + 16] for i in range(0, LENGTH, 16)])
    return password


@simple_filter
def prefix_extract(value):
    """ Gets the first part of a customer name as the suggested prefix """
    name = value.replace(string.punctuation, ' ')
    return name.split(' ')[0].upper()[:4]

