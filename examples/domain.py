from ldap3 import SUBTREE, Server, Connection, ALL
import json

ad_server = Server('testdomaincontroller', get_info=ALL)
username = "FUN\\alice"
password = "testpw"

with Connection(ad_server, username, password, auto_bind=True) as conn:
    any_filter = '(objectClass=domain)'

    base_dn = 'dc=FUN,dc=com'

    conn.search(search_base=base_dn, search_filter=any_filter,
                search_scope=SUBTREE)

    for entry in conn.entries:
        print(entry.entry_to_json())
        print('------------------')

conn.unbind()
