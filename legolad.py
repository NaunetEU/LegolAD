import argparse
from models import Arguments
from functions import custom, spn, computers
from logger import log, change_output_file

# example usage:
# python3 legolad.py -mi 2 -ma 60 -p 10 -t 192.168.1.12 -fu spn

# for custom filter:
# python3 legolad.py -mi 2 -ma 60 -p 10 -t 192.168.1.12 -fu custom -fi "(|(objectClass=group)(objectClass=user))"

# I recommend page size of 10 for stealthy enumeration

# I recommend 2-60 sec for spn enumeration (average 31 sec), therefore in case of 5000 users it would take
# 5000 names / 10 names per page * 31 sec = 15500 sec = 4.3 hours

# I recommend 2-5 sec for very specific computer enumeration


def args() -> Arguments:
    # parse arguments
    general_help = "Please provide credentials in the .env file based on the .env.example file."
    parser = argparse.ArgumentParser(description=general_help)
    parser.add_argument("--min-time-to-sleep", '-mi', type=int, default=0,
                        help="Minimum time to sleep in seconds. In case of --burst, this is minimum random seconds between bursts.")
    parser.add_argument("--max-time-to-sleep", '-ma', type=int, default=0,
                        help="Maximum time to sleep in seconds. In case of --burst, this is maximum random seconds between bursts.")
    parser.add_argument("--page-size", '-p', type=int,
                        default=10, help="Number of results per page")
    parser.add_argument("--dc-target", '-t', type=str, required=True,
                        help="Domain controller IP address or hostname")
    parser.add_argument("--ldap-attributes", '-a', nargs='+', default=[],
                        help="List of LDAP attributes to return for example: cn, mail, memberOf... for more, please check https://docs.bmc.com/docs/fpsc121/ldap-attributes-and-associated-fields-495323340.html")
    parser.add_argument("--filter", '-fi', type=str, default="",
                        help="In case of spn, this is ignored, in case of computers a string that must be in the computer name, in case of custom, a valid LDAP filter.")
    parser.add_argument("--function", '-fu', type=str, required=True,
                        help="spn for people, computers for computers, custom for you custom LDAP filter provided in --filter")
    parser.add_argument("--output", '-o', type=str, default="output.json",
                        help="Output file name, default is output.json")

    parser.add_argument("--breaks", "-br", nargs='+', action='append',
                        default=[], help="Break: -br 12:00 13:00 -br 13:10 13:20")

    parser.add_argument('--burst', '-b', type=int, default=0,
                        help="Number of pages to request in a burst")

    # --ssl true/false action='store_true'
    parser.add_argument('--ssl', '-s', help="Use SSL", action='store_true')

    username = ''
    password = ''
    domain_root = ''

    # read username and password from .env file, be aware of quotes and whitespaces
    with open(".env", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("username"):
                username = line.split("=")[1].strip()
                # strip quotes if present
                if username.startswith("\"") and username.endswith("\""):
                    username = username[1:-1]
            elif line.startswith("password"):
                password = line.split("=")[1].strip()
                # strip quotes if present
                if password.startswith("\"") and password.endswith("\""):
                    password = password[1:-1]
            elif line.startswith("domain_root"):
                domain_root = '='.join(line.split("=")[1:])
                domain_root = domain_root.strip()
                # strip quotes if present
                if domain_root.startswith("\"") and domain_root.endswith("\""):
                    domain_root = domain_root[1:-1]

    parser = parser.parse_args()
    # create ret as an Arguments object
    ret = Arguments(
        min_time_to_sleep=parser.min_time_to_sleep,
        max_time_to_sleep=parser.max_time_to_sleep,
        domain_root=domain_root,
        page_size=parser.page_size,
        username=username,
        password=password,
        dc_target=parser.dc_target,
        ldap_attributes=parser.ldap_attributes,
        filter=parser.filter,
        function=parser.function,
        output=parser.output,
        breaks=parser.breaks,
        burst=parser.burst,
        ssl=parser.ssl
    )

    # set OUTPUT_FILE
    change_output_file(ret.output)

    return ret


def main():
    arguments = args()
    if arguments.function == 'spn':
        spn.run(arguments)
    elif arguments.function in ['computers', 'computer']:
        computers.run(arguments)
    elif arguments.function == 'custom':
        custom.run(arguments)
    else:
        print('No function specified.')


if __name__ == "__main__":
    main()
