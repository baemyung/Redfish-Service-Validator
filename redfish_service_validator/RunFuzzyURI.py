
import os
import sys
import argparse
import logging


tool_version = '2.2.6'

# Set up the custom debug levels
VERBOSE1=logging.INFO-1
VERBOSE2=logging.INFO-2

logging.addLevelName(VERBOSE1, "VERBOSE1")
logging.addLevelName(VERBOSE2, "VERBOSE2")

def verbose1(self, msg, *args, **kwargs):
    if self.isEnabledFor(VERBOSE1):
        self._log(VERBOSE1, msg, args, **kwargs)

def verbose2(self, msg, *args, **kwargs):
    if self.isEnabledFor(VERBOSE2):
        self._log(VERBOSE2, msg, args, **kwargs)
        
logging.Logger.verbose1 = verbose1
logging.Logger.verbose2 = verbose2

my_logger = logging.getLogger()
my_logger.setLevel(logging.DEBUG)
standard_out = logging.StreamHandler(sys.stdout)
standard_out.setLevel(logging.INFO)
my_logger.addHandler(standard_out)

status_code = 1

def main(argslist=None, configfile=None):
    """Main command

    Args:
        argslist ([type], optional): List of arguments in the form of argv. Defaults to None.
    """    
    argget = argparse.ArgumentParser(description='DMTF tool to test a service against a collection of Schema, version {}'.format(tool_version))

    # fuzzier options
    argget.add_argument('--in_uri_list', '-i', type=str, help='Filename with the visited uris')
    argget.add_argument('--out_uri_list', '-o', type=str, help='File to save the fuzzy  uris')

    # parse...
    args = argget.parse_args(argslist)
    input_file = args.in_uri_list
    output_file = args.out_uri_list

    lastResultsPage = output_file

    if os.path.exists(input_file):
        with open(input_file,'r') as f_in:
            with open(output_file,'w') as f_out:
                for line in f_in:
                    parts = line.strip().split('/')
                    # Try with the last part variation
                    fuzzy_uri = '/'.join(parts[:-1]) + "/X" + parts[-1] + "Z"
                    f_out.write(fuzzy_uri + '\n')
                    if(len(parts) > 6):
                        # Try with the additional part variation 2
                        fuzzy_uri = '/'.join(parts[:-3]) + "/X" + parts[-3] + "Z/" + parts[-2] + "/" + parts[-1]
                        f_out.write(fuzzy_uri + '\n')

    return status_code, lastResultsPage, 'Validation done'


if __name__ == '__main__':
    status_code, lastResultsPage, exit_string = main()
    sys.exit(status_code)
