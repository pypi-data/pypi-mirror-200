"""In due time (Finnish: ajallaan) - reporting on worklog entries of some ticket system - api"""
import argparse
import datetime as dti
import json
import logging
import operator
import pathlib
import sys
from typing import no_type_check

from ajallaan import (
    API_TOKEN,
    API_USER,
    DEBUG,
    ENCODING,
    QUIET,
    Scope,
    VERBOSE,
    WORKLOG_AUTHOR,
    log,
)

USER_KEY = 'u14826'
EPH_TITLE = 'EPIC-TITLE-MISSING-IN-DATA'
workdays = {
    '01': 21,
    '02': 20,
    '03': 23,
    '04': 18,
    '05': 20,
    '06': 20,
    '07': 21,
    '08': 21,
    '09': 21,
    '10': 22,
    '11': 21,
    '12': 15,
}


@no_type_check
def behind_the_moon():
    """Spike content in here or empty (goal)."""
    year_wds = sum(workdays.values())
    first_hour = 4
    last_hour = 18
    source = sys.argv[1]
    year = 2023
    # f'worklog-monthly-{year}-{mm}-to-date-{to_date}.json'
    # assume 2023 for now, ...
    mm = source.lstrip('./').replace(f'worklog-monthly-{year}-', '', 1).split('-', 1)[0]

    mm_wds = workdays[mm]

    def my_time(epocms: int) -> str:
        """Convert EPOC timestamp to local ISO string."""
        return dti.datetime.fromtimestamp(epocms // 1000).strftime('%Y-%m-%d %H:%M:%S')

    def my_duration(seconds: int) -> float:
        """Convert number of seconds to fractional hours."""
        return seconds / 3600.0

    worklog = json.load(open(source, 'rt', encoding=ENCODING))
    print(len(worklog['projects']))

    pi_counts = [[i['key'] for i in p['issues']] for p in worklog['projects']]
    print(pi_counts)

    my_hours = 0
    my_wls = {}
    issue_titles = {}
    epic_of = {}
    for project in worklog['projects']:
        p_key = project['key']
        my_wls[p_key] = {}
        for issue in project['issues']:
            i_key = issue['key']
            epic_of[i_key] = issue.get('epicKey', 'MISSING-EPIC')
            issue_titles[i_key] = issue['summary']
            my_wls[p_key][i_key] = []
            for entry in issue['workLogs']:
                if entry['authorUserKey'] == USER_KEY:
                    these_hours = my_duration(entry['timeSpent'])
                    my_hours += these_hours
                    my_wls[p_key][i_key].append(
                        (
                            my_time(entry['workStart']),
                            these_hours,
                            entry['comment'],
                        )
                    )

    daily = {}
    suspicious_start = []
    epic_totals = {v: 0.0 for v in epic_of.values()}
    for p_key in my_wls.keys():
        print(f'{p_key}:')
        for i_key in my_wls[p_key].keys():
            th_issue = sum(duration for (_, duration, _) in my_wls[p_key][i_key])
            epic_totals[epic_of[i_key]] += th_issue
            if th_issue > 0:
                print(f'- {i_key} - ({issue_titles[i_key]}) - total hours = {round(th_issue, 2) :.2f}:')
                for start, duration, comment in my_wls[p_key][i_key]:
                    print(f'  + {start}: {round(duration, 2) :.2f} hours - {comment}')
            for start, duration, comment in my_wls[p_key][i_key]:
                date_slot = start[:10]
                if date_slot not in daily:
                    daily[date_slot] = 0.0
                daily[date_slot] += duration
                hour_code = start[11:13]
                hour_num = int(hour_code)
                if not (first_hour <= hour_num <= last_hour):
                    suspicious_start.append((i_key, issue_titles[i_key], start))

    print(f'Total: {round(my_hours, 2) :.2f} hours')

    print('Hours per Epic:')
    epic_totals = dict(reversed(sorted(epic_totals.items(), key=operator.itemgetter(1))))
    for epic_key, th_epic in epic_totals.items():
        if th_epic > 0 and epic_key != 'MISSING-EPIC':
            title = issue_titles.get(epic_key, EPH_TITLE)
            print(f'- {epic_key} - ({title}) - total hours = {round(th_epic, 2) :.2f}:')

    if 'MISSING-EPIC' in epic_totals:
        print('Hours without Epic:')
        th_wo_epic = epic_totals['MISSING-EPIC']
        if th_wo_epic > 0:
            print(f'- MISSING-EPIC - {EPH_TITLE} - total hours = {round(th_wo_epic, 2) :.2f}:')

    print(f'Workdays of {year}-{mm}: {mm_wds}')
    print(f'Workdays of full {year}: {year_wds}')
    print(f'Hours of contract for {year}-{mm}: {round(mm_wds * 8.6667, 2) :.2f}')

    print('Hours per workday:')
    daily = dict(sorted(daily.items(), key=operator.itemgetter(0)))
    delta_mm = 0
    for date_slot, hours in daily.items():
        if hours > 0:
            delta = hours - 8.6667
            delta_mm += delta
            print(
                f'- {date_slot} total hours = {round(hours, 2) :.2f}'
                f' -> {round(delta_mm, 2) :+.2f} ({round(delta, 2) :+.2f})'
            )

    print(f'Monthly contract balance is {round(my_hours, 2) :.2f} -> Delta = {round(delta_mm, 2) :+.2f}')

    if suspicious_start:
        print(
            f'WARNING: {len(suspicious_start)} worklog entries found with'
            f' suspicious start times outside of [{first_hour}, {last_hour}] UTC:'
        )
        for key, title, start in suspicious_start:
            print(f'- {start}: {key} - {title}')


@no_type_check
def process(options: argparse.Namespace):
    """Process the command line request."""
    if not options:
        log.error('no data given to process')
        return 1

    global DEBUG
    if options.debug:
        DEBUG = True

    global VERBOSE
    if options.verbose:
        VERBOSE = True

    global QUIET
    if options.quiet:
        QUIET = True

    if QUIET:
        DEBUG = VERBOSE = not QUIET

    if DEBUG:
        log.setLevel(logging.DEBUG)
        log.debug('log level debug requested')
    elif QUIET:
        log.setLevel(logging.ERROR)

    scope = Scope.LOCAL
    if not (options.user and options.token or API_USER and API_TOKEN):
        log.info('entering local mode as no coherent credentials found')
        in_path = pathlib.Path(options.in_path)
        if not in_path.is_file() or not in_path.stat().st_size:
            log.error(f'given path ({in_path}) is either no file or has no content')
            return 1

        try:
            data = json.load(in_path.open())
        except RuntimeError as err:
            log.error(f'parsing path ({in_path}) as json failed with error ({err})')
            return 1
        log.warning(
            f'would process local data of {sys.getsizeof(data)} bytes in host memory'
            ' for worker inherent in data'
        )
        return 0

    if options.in_path:
        log.error('why use api user and token when local input is given - confusion leads to error')
        return 2

    if not options.worker and not WORKLOG_AUTHOR:
        log.info(f'setting worker equal to api user ({options.user})')
        options.worker = options.user or API_USER

    scope = Scope.REMOTE
    log.warning('would fetch the worklog data using the given coordinates and credentials')
    return 0
