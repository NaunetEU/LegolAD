# LegolAD

LegolAD is a lightweight Python tool for performing LDAP enumeration. It supports three main modes of operation:

- spn – for enumerating Service Principal Names
- computers – for listing computer accounts in Active Directory
- custom – for running fully customized LDAP queries using your own filters

It’s designed to be flexible, allowing you to adjust query speed, result size, and filtering options to suit your environment or use case.
Installation

## Clone the repository:

```
git clone https://github.com/NaunetEU/LegolAD.git
cd LegolAD
```

## Install requirements (tested on Python 3.11):

```
pip install -r requirements.txt
```

## Set up a .env file based on .env.example and provide your LDAP credentials and domain root:

username="your_username"
password="your_password"
domain_root="DC=example,DC=com"

Note: The values need to be quoted. No leading or trailing whitespace.
Usage

LegolAD is run from the command line:

```
python3 legolad.py [options]
```

At a minimum, you must specify:

```
--dc-target (or -t) – IP address or hostname of the domain controller
--function (or -fu) – the mode to run in: spn, computers, or custom
```

Each mode works a little differently:
### Mode: spn

This mode ignores any provided filter. It retrieves all accounts with SPNs, useful for identifying Kerberoastable accounts.

Example:

```
python3 legolad.py -t 192.168.1.12 -fu spn -mi 2 -ma 60 -p 10
```

### Mode: computers

This mode expects a string in the --filter parameter. It returns computer objects whose names contain that string.

Example:

```
python3 legolad.py -t 192.168.1.12 -fu computers -fi "SERVER" -mi 2 -ma 5 -p 10
```

### Mode: custom

This lets you provide a full LDAP filter expression using the --filter parameter.

Example:

```
python3 legolad.py -t 192.168.1.12 -fu custom -fi "(|(objectClass=group)(objectClass=user))" -p 10
```

## Command-Line Arguments

```
--dc-target	-t	Required. Domain controller IP or hostname.
--function	-fu	Required. One of: spn, computers, or custom.
--filter	-fi	Depends on mode. Ignored for spn. For computers, it's a name match string. For custom, it's a full LDAP filter.
--ldap-attributes	-a	Comma-separated list of LDAP attributes to return (e.g. cn,mail).
--output	-o	Output filename. Defaults to output.json.
--page-size	-p	Number of results per page. Default is 10.
--min-time-to-sleep	-mi	Minimum sleep time (in seconds) between requests.
--max-time-to-sleep	-ma	Maximum sleep time (in seconds) between requests.
--burst	-b	Number of pages to fetch in one burst before sleeping.
--breaks	-br	Pause during defined time ranges. Use multiple: -br 12:00 13:00 -br 13:30 14:00
--ssl	-s	Use SSL for the LDAP connection.
```
