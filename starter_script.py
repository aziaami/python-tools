#!/usr/bin/env python

import os
import sys
import time
import datetime
import logging
import traceback
from optparse import OptionParser

# -----------------------------------------------------------------------------


def HelloWorld():
    '''Print and log Hello World !'''
    print('Hello World !')
    print('... waiting for 5 seconds ...')

    time.sleep(5)   # Sleep
    print('... finished waiting ...')
    logging.info('Hello Log file !')

# -----------------------------------------------------------------------------
# this is executed when we run this script from commandline
if __name__ == '__main__':
    usage = """%prog - Script to use so we don't have to start from scratch every time."""
    parser = OptionParser(usage=usage)

    try:
        ## ===== Input arguments ================
        parser.add_option("--log_to_file",
                          action="store_true", dest="log_info_to_file",
                          default=False,
                          help="Set true to log info to file. default:false.")
        parser.add_option("--log_dir",
                          action="store", type="string", dest="log_dir",
                          default="/tmp",
                          help="Log files are written into this directory. default:/tmp")
        parser.add_option("--dry-run",
                          action="store_true", dest="dry-run", default=False)
        parser.add_option("-r", "--raw_logs_root",
                          action="store", type="string", dest="raw_logs_root",
                          default="/data/logs",
                          help="Root directory of the data logs. default:/data/logs")

        # add arguments here

        ## ======================================

        (options, args) = parser.parse_args()

        # Open logfile.
        start_time_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        log_directory_name = os.path.join(options.log_dir, '%prog-%s.log' % start_time_str)
        FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'

        if options.log_info_to_file:
            logging.basicConfig(filename=log_directory_name, level=logging.DEBUG, format=FORMAT)
            print '===> Running with logfile: %s' % log_directory_name
        else:
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)

        # ======= Validate input arguments ================
        if not options.raw_logs_root or not os.path.exists(options.raw_logs_root):
            logging.critical('raw_logs_root must be specified, and must exist: %s',
                             options.raw_logs_root)
            sys.exit(-1)

        # validate other input args here

        ## ================================================

        # Print out configuration at the start for reference in a log file
        logging.info('Running with configuration:')
        logging.info(parser.parse_args())

        ## ====== SCRIPT CODE HERE ========================

        HelloWorld()

    ## ================================================
    except KeyboardInterrupt, e:  # Ctrl-C
        print('Ctrl-C pressed')
        raise e
    except SystemExit, e:  # sys.exit()
        raise e
    except Exception, e:
        print('Unexpected exception - logging error')
        logging.critical(str(e))
        traceback.print_exc()
        os.exit(1)
