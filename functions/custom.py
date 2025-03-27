from models import Arguments
from logger import log, save_json
from ldapper import query


def run(arguments: Arguments):
    # create ad servers
    if arguments.filter == "":
        print("Please specify a filter by using --filter or -fi")
        return
    ldap_filter = arguments.filter
    results = query(arguments, ldap_filter)
    save_json(results)