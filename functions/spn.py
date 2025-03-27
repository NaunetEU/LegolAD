from models import Arguments
from logger import log, save_json
from ldapper import query


def run(arguments: Arguments):
    ldap_filter = "(&(objectClass=user)(objectCategory=user)(servicePrincipalName=*))"
    results = query(arguments, ldap_filter)
    save_json(results)