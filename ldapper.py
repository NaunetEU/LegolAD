from ldap3 import Server, Connection, ALL, SUBTREE, core, NONE
import random
import time
import json
from logger import log
from models import Arguments
from datetime import datetime
import pytz


def should_we_break(arguments: Arguments) -> bool:
    # set the timezone to Europe/Budapest
    tz = pytz.timezone('Europe/Budapest')

    # get the current time
    now = datetime.fromtimestamp(time.time(), tz)

    for break_session in arguments.breaks:
        raw_start = break_session[0]
        raw_end = break_session[1]

        start = datetime.strptime(
            f'{now.year}-{now.month}-{now.day} {raw_start}:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(
            f'{now.year}-{now.month}-{now.day} {raw_end}:00', '%Y-%m-%d %H:%M:%S')

        start = tz.localize(start)
        end = tz.localize(end)

        print([start, now, end])

        if start < now and now < end:
            time_until_break_ends = (end - now).total_seconds()
            return True, time_until_break_ends
    return False, 0


def snooze(arguments: Arguments, total_entries: int):
    is_in_break, time_until_break_ends = should_we_break(arguments)
    if is_in_break:
        hours = int(time_until_break_ends / 3600)
        minutes = int((time_until_break_ends - hours * 3600) / 60)
        seconds = int(time_until_break_ends - hours * 3600 - minutes * 60)

        print(
            f'[BREAK] We are in a break session, sleeping for {hours} h, {minutes} m, {seconds} s ...')
        time.sleep(time_until_break_ends)

    if arguments.burst > 0:
        # if we are in burst mode, we sleep after every burst
        if total_entries % arguments.page_size == 0:
            pages_retrieved = total_entries / arguments.page_size
            if pages_retrieved % arguments.burst == 0:
                rand_sleep = random.randint(
                    arguments.min_time_to_sleep, arguments.max_time_to_sleep)
                print(
                    f'[SLEEP] Sleeping for {rand_sleep} seconds until next burst.............................................................')
                print('\n')
                time.sleep(rand_sleep)
    else:
        # no burst mode, we sleep after every page which is divisible by page_size
        if total_entries % arguments.page_size == 0:
            rand_sleep = random.randint(
                arguments.min_time_to_sleep, arguments.max_time_to_sleep)
            print(
                f'[SLEEP] Sleeping for {rand_sleep} seconds.............................................................')
            print('\n')
            time.sleep(rand_sleep)


def query(arguments: Arguments, filter: str) -> list:
    # create ad servers
    ret = []
    if arguments.ssl:
        ad_server = Server(arguments.dc_target, get_info=NONE, use_ssl=True)
    else:
        ad_server = Server(arguments.dc_target, get_info=NONE, use_ssl=False)

    total_entries = 0

    with Connection(ad_server, arguments.username, arguments.password, auto_bind=True) as conn:

        entry_generator = conn.extend.standard.paged_search(
            search_base=arguments.domain_root,
            search_filter=filter,
            search_scope=SUBTREE,
            attributes=arguments.ldap_attributes,
            paged_size=arguments.page_size,
            paged_criticality=True,
            generator=True
        )

        for entry in entry_generator:
            total_entries += 1
            ret.append(entry)
            entry_as_string = str(entry)
            log(entry_as_string.replace('\n', ' '))
            try:
                snooze(arguments, total_entries)
                # if we get a KeyboardInterrupt, we want to stall
            except KeyboardInterrupt:
                try:
                    input('\nStalling... Press any key to continue...')
                except KeyboardInterrupt:
                    save = input('\nSave before exiting? [Y/n]')
                    if save.lower() == 'y' or save.lower() == 'yes' or save == '':
                        ret_jsonable = []
                        for entry_to_save in ret:
                            if 'uri' in entry_to_save:
                                to_append = {
                                    'uri': entry_to_save['uri'],
                                    'type': entry_to_save['type'],
                                }
                            else:
                                to_append = {
                                    "attributes": dict(entry_to_save['attributes']),
                                    "dn": entry_to_save['dn']
                                }
                            ret_jsonable.append(to_append)
                        return ret_jsonable
                    else:
                        exit()

    log(f'[INFO] DONE, {total_entries} entries retrieved.')
    ret_jsonable = []
    for entry in ret:
        if 'uri' in entry:
            to_append = {
                'uri': entry['uri'],
                'type': entry['type'],
            }
        else:
            to_append = {
                "attributes": dict(entry['attributes']),
                "dn": entry['dn'],
            }

        ret_jsonable.append(to_append)

    return ret_jsonable
