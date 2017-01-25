#!/usr/bin/env python

import os
import sys
import time
import datetime
import logging
import traceback
from optparse import OptionParser
import sqlite3

# -----------------------------------------------------------------------------
# user functions here


# -----------------------------------------------------------------------------
# this is executed when we run this script from commandline
if __name__ == '__main__':
    usage = """%prog - Script to query sqlite database."""
    parser = OptionParser(usage=usage)

    try:
        parser.add_option("--log_info_to_file",
                          action="store_true", dest="log_info_to_file",
                          default=False,
                          help="Set true to log info to file. default:false.")
        parser.add_option("--log_dir",
                          action="store", type="string", dest="log_dir",
                          default="/tmp",
                          help="Log files are written into this directory. default:/tmp")
        parser.add_option("--dry-run",
                          action="store_true", dest="dry-run", default=False)
        parser.add_option("-db", "--database",
                          action="store", type="string", dest="database",
                          default="",
                          help="path to sqlite database file.")

        # ======================================

        (options, args) = parser.parse_args()

        # Open logfile.
        start_time_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
        log_directory_name = os.path.join(
            options.log_dir, 'query_sqlite_db-%s.log' % start_time_str)
        FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'

        if options.log_info_to_file:
            logging.basicConfig(filename=log_directory_name,
                                level=logging.DEBUG, format=FORMAT)
            print '===> Running with logfile: %s' % log_directory_name
        else:
            logging.basicConfig(level=logging.DEBUG, format=FORMAT)

        # Validate input arguments.
        if not os.path.exists(options.database):
            logging.critical('database file not found : %s',
                             options.database)
            sys.exit(-1)

        # ================================================

        # Print out configuration at the start for reference in a log file
        logging.info('Running with configuration:')
        logging.info(parser.parse_args())

        # ====== SCRIPT CODE HERE ========================

        conn = sqlite3.connect(options.database)
        cursor = conn.cursor()

        sql = "SELECT node_id FROM graph_rootnode"
        logging.info(sql)

        #cursor.execute(sql, [("Red")])
        #result = cursor.fetchall()
        # logging.info(result)

        logging.info("list of records in table:")
        for row in cursor.execute(sql):
            logging.info(row)
        # ================================================
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
