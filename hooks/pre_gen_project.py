import re
import sys

HOSTNAME = '{{ cookiecutter.hostname }}'
DOMAIN = '{{ cookiecutter.domain }}'
XGS_IP_ADDRESS = '{{ cookiecutter.xgs_tanker_ip }}'


def is_domain(value: str) -> bool:
    if not value:
        return False
    try:
        return not re.search(r"\s", value) and re.match(
            # First character of the domain
            rf"^(?:[a-zA-Z0-9]"
            # Sub domain + hostname
            + r"(?:[a-zA-Z0-9-_]{0,61}[A-Za-z0-9])?\.)"
            # First 61 characters of the gTLD
            + r"+[A-Za-z0-9][A-Za-z0-9-_]{0,61}"
            # Last character of the gTLD
            + rf"[A-Za-z]$",
            value.encode("idna").decode("utf-8"),
            re.IGNORECASE,
        )
    except UnicodeError:
        return False


def legal_domain(value: str) -> bool:
    if 'kunde.de' in value: return False
    if 'rausys.de' in value: return False
    return True


for _d in [HOSTNAME, DOMAIN]:
    if not is_domain(_d) or not legal_domain(_d):
        print(f'ERROR: "{_d}" is not a valid hostname!')
        sys.exit(1)

if XGS_IP_ADDRESS == '192.168.0.0' or not XGS_IP_ADDRESS:
    print(f'ERROR: "{XGS_IP_ADDRESS}" is not a valid XGS IP address')
