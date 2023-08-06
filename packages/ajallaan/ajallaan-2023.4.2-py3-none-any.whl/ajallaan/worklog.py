"""In due time (Finnish: ajallaan) - reporting on worklog entries of some ticket system - fetch worklog"""
import datetime as dti
import json
from typing import no_type_check

import httpx
from ajallaan import ENCODING, log

TS_FORMAT = '%Y-%m-%d %H:%M:%S.%f +00:00'
TS_FORMAT_SLUG = '%Y%m%dT%H%M%SZ'


@no_type_check
def behind_the_moon():
    """Spike content in here or empty (goal)."""
    end_dd = {
        '01': '31',
        '02': '28',
        '03': '31',
        '04': '30',
        '05': '31',
        '06': '30',
        '07': '31',
        '08': '31',
        '09': '30',
        '10': '31',
        '11': '30',
        '12': '31',
    }
    to_date = dti.datetime.now(tz=dti.timezone.utc).strftime(TS_FORMAT_SLUG)
    year = 2023
    mm = '03'
    end_mm_dd = end_dd[mm]
    user = 'thewun'
    token = None
    max_results = 1000
    wl_user = user
    protocol = 'https'
    host = 'example.com'
    api_root = '/rest/com.deniz.jira.worklog/1.0/timesheet/'
    perspective = 'user'
    url = (
        f'{protocol}://{host}{api_root}{perspective}?'
        f'targetKey={wl_user}&startDate={year}-{mm}-1&endDate={year}-{mm}-{end_mm_dd}&maxResults={max_results}'
    )

    log.info(f'Using URL ({url}) for ({year}-{mm}) ...')
    try:
        r = httpx.get(url, auth=(user, token))
    except httpx.RequestError as exc:
        log.error(f'An error occurred while requesting {exc.request.url!r}.')

    fname = f'worklog-monthly-{year}-{mm}-to-date-{to_date}.json'
    with open(fname, 'wt', encoding=ENCODING) as handle:
        json.dump(r.json(), handle)

    log.info(f'wrote worklog data to ({fname})')
