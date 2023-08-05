import os
import sys
import json
import argparse
import logging

logging.basicConfig(filename = "diwier.log", level=logging.DEBUG)

# initiate logger
logger = logging.getLogger(__name__)

# creating parser object
class ArgsParser(argparse.ArgumentParser):
	def error(self, message):# Modified to show help text on error
		sys.stderr.write('\033[0;31merror: %s\n\n\033[0m' % message)
		self.print_help()
		sys.exit(2)

parser = ArgsParser()
# adding arguments

parser.add_argument('-t', '--script-type', required=True, nargs=1, metavar='purge|purge-no-backup|backup|migrate')
parser.add_argument('-s', '--source', required=True, nargs=1, metavar='Source DB URL') # dialect://username:password@host:port/extensions
parser.add_argument('-sd', '--source-dialect', required=True, nargs=1, metavar='SQLAlchemy supported dialect')
parser.add_argument('-d', '--destination', required=False, nargs=1, metavar='Destination DB URL') # dialect+driver://username:password@host:port/?service_name=service
parser.add_argument('-dd', '--destination-dialect', required=False, nargs=1)


def run():
    global parser, logger
    script_types = {'purge', 'purge-no-backup', 'backup', 'migrate'}
    args = parser.parse_args()
    logger.info("Initiatialising")

    req_script = None
    if args.script_type is not None and args.script_type[0] in script_types:
        req_script = args.script_type[0]
    else :
        print('Unidenitifed argument type')
        return
    

    # if args.test is not None:
    #     from .scanner import scan
    #     for src in args.test:
    #         urls = scan(src, debug=True)
    #     return

    # if args.sources is not None:
    #     source = args.sources[0]
    #     if not os.path.isfile(args.sources[0]):
    #         logger.error("Sources were not found. Exiting.")
    #         sys.exit(0)
    #     else:
    #         logger.info("Attempting source load")
    
    parser.print_help()