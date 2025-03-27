from ldap3 import Server, Connection, ALL
import json

ad_server = Server('192.168.1.12', get_info=ALL)
username = "FUN\\alice"
password = "bubbles1"

with Connection(ad_server, username, password, auto_bind=True) as conn:
    ldap_filter = f'(sAMAccountName={username})'

    any_filter = '(objectClass=computer)'

    base_dn = 'dc=FUN,dc=com'
    result = conn.search(search_base=base_dn,
                         search_filter=any_filter, attributes=['memberOf'])

    for entry in conn.entries:
        parsed_entry = json.loads(entry.entry_to_json())
        print(parsed_entry["attributes"]["memberOf"])
        print(parsed_entry["dn"])
        print('------------------')

conn.unbind()
