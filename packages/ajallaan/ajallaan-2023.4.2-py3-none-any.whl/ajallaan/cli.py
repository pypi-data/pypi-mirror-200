"""In due time (Finnish: ajallaan) - reporting on worklog entries of some ticket system - command line interface"""
import argparse
import sys
from typing import no_type_check

import ajallaan.api as api
from ajallaan import APP_NAME, APP_VERSION


@no_type_check
def parser():
    """Implementation of command line API returning parser."""
    impl = argparse.ArgumentParser(
        description='Showcase (Finnish: vitriini) some packaged content - guided by conventions.'
    )
    impl.add_argument(
        '-q',
        '--quiet',
        dest='quiet',
        action='store_true',
        help='Be quiet (overrules debug and verbose alike)',
    )
    impl.add_argument(
        '-v',
        '--verbose',
        dest='verbose',
        action='store_true',
        help='Be more verbose, maybe',
    )
    impl.add_argument(
        '-d',
        '--debug',
        dest='debug',
        action='store_true',
        help='Support debugging, maybe',
    )
    impl.add_argument(
        '-i',
        '--input',
        dest='in_path',
        type=str,
        required=False,
        help='Input path of local data',
    )
    impl.add_argument(
        '-u',
        '--user',
        dest='user',
        type=str,
        required=False,
        help='API user account name',
    )
    impl.add_argument(
        '-t',
        '--token',
        dest='token',
        type=str,
        required=False,
        help='API token or passphrase',
    )
    impl.add_argument(
        '-w',
        '--worker',
        dest='worker',
        type=str,
        required=False,
        help='Worklog user name whose entries to report (default is api user)',
    )
    impl.add_argument(
        '-o',
        '--output',
        dest='out_path',
        type=str,
        required=False,
        help='Output path for json report',
    )
    return impl


@no_type_check
def app(argv=None):
    """Drive the transformation."""
    argv = sys.argv[1:] if argv is None else argv
    arg_parser = parser()
    if not argv:
        print(f'{APP_NAME} version {APP_VERSION}')
        arg_parser.print_help()
        return 0

    options = arg_parser.parse_args(argv)
    return api.process(options)
