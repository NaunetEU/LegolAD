from ldapper import query
from logger import log, save_json
from models import Arguments


def run(arguments: Arguments):
    if arguments.filter == "":
        ldap_filter = "(&(objectClass=Computer)(name=*))"
    else:
        ldap_filter = f"(&(objectClass=Computer)(name=*{arguments.filter}*))"
    results = query(arguments, ldap_filter)
    save_json(results)
