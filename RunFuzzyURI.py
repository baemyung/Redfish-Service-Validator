#!/usr/bin/env python3

from redfish_service_validator.RunFuzzyURI import main
import sys

if __name__ == '__main__':
    status_code, lastResultsPage, exit_string = main()
    sys.exit(status_code)
