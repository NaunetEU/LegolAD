from ldap3 import SUBTREE, Server, Connection, ALL
import json

ad_server = Server('testdomaincontroller', get_info=ALL)
username = "FUN\\alice"
password = "testpw"

with Connection(ad_server, username, password, auto_bind=True) as conn:
    ldap_filter = f'(sAMAccountName={username})'

    any_filter = '(objectClass=*)'

    base_dn = 'dc=FUN,dc=com'

    account_name = 'sAMAccountName'
    common_name = 'cn'
    account_expire = 'accountExpires'
    admin_count = 'adminCount'
    sid = 'objectSid'
    object_guid = 'objectGUID'
    object_category = 'objectCategory'
    object_class = 'objectClass'
    user_principal_name = 'userPrincipalName'
    when_created = 'whenCreated'
    when_changed = 'whenChanged'

    attributes = [
        account_name,
        common_name,
        account_expire,
        admin_count,
        sid,
        object_guid,
        object_category,
        object_class,
        user_principal_name,
        when_created,
        when_changed
    ]
    conn.search(search_base=base_dn, search_filter=any_filter,
                search_scope=SUBTREE)

    for entry in conn.entries:
        print(entry.entry_to_json())
        print('------------------')

conn.unbind()
