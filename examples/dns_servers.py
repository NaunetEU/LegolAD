from ldap3 import Server, Connection, ALL, SUBTREE
import json

ad_server = Server('testdomaincontroller', get_info=ALL)
username = "FUN\\alice"
password = "testpw"

with Connection(ad_server, username, password, auto_bind=True) as conn:
    dns_base_dn = '(CN=fun,CN=com)'
    any_filter = '(objectClass=dnsNode)'

    base_dn = 'dc=FUN,dc=com'
    result = conn.search(search_base=base_dn,
                         search_filter=any_filter, search_scope=SUBTREE)

    for entry in conn.entries:
        print(entry.entry_to_json())
        parsed_entry = json.loads(entry.entry_to_json())
        print('-----------')

conn.unbind()
