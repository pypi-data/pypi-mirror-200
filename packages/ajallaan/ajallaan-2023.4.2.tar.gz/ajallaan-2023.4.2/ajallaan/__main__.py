"""In due time (Finnish: ajallaan) - reporting on worklog entries of some ticket system - module call enabler"""
import sys

from ajallaan.cli import app

if __name__ == '__main__':
    sys.exit(app(sys.argv[1:]))  # pragma: no cover
