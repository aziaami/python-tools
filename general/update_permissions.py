#!/usr/bin/python

# Python script to update permissions of all files in a root directory

import os,sys,datetime,logging
from optparse import OptionParser

# -----------------------------------------------------------------------------
def update_permissions(some_path):
    logging.info(some_path)
    if not options.dry_run:
        os.chmod(some_path, options.permission)
# -----------------------------------------------------------------------------
def os_walk(some_path):
    '''function executed by walk in every new folder'''
    logging.info('Walking down root directory: ' + some_path)
    for path, dirnames, filenames in os.walk(some_path):
      for dirname in dirnames:
        update_permissions(os.path.join(path, dirname))

      for filename in filenames:
        update_permissions(os.path.join(path, filename))

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    usage = "%prog - Update permissions in a given root directory"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--root_dir",
                      action="store", type="string", dest="root_dir",
                      default="")
    parser.add_option("-p", "--permission",
                      action="store", type="int", dest="permission",
                      default=0777,
                      help="New permission as Octal integer literal")
    parser.add_option("--dry_run",
                      action="store_true", dest="dry_run",
                      default=False,
                      help='print output without changing any files')
    parser.add_option("--log_dir",
                      action="store", type="string", dest="log_dir",
                      default="/tmp",
                      help="Logfiles are written into this directory.")
    parser.add_option("--log_info_to_file",
                      action="store_true", dest="log_info_to_file",
                      default=False)
    (options, args) = parser.parse_args()

    # Open logfile.
    if not options.log_dir or not os.path.exists(options.log_dir):
        logging.critical('log_dir must exist: %s', options.log_dir)
        sys.exit(-1)
    start_time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    log_directory_name = os.path.join(options.log_dir, 'DataLoggingMonitor-%s.log' % start_time_str)
    FORMAT = '%(asctime)-15s %(levelname)-8s %(message)s'
    if options.log_info_to_file:
        logging.basicConfig(filename=log_directory_name, level=logging.DEBUG, format=FORMAT)
        print '===> Running with logfile: %s' % log_directory_name
    else:
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    logging.info('Running with configuration:')
    logging.info(parser.parse_args())

    # check root directory
    if not options.root_dir or not os.path.exists(options.root_dir):
        logging.critical('root directory does not exist: %s', options.root_dir)
        sys.exit(-1)

    logging.info('Updaing permissions to: ' + str(oct(options.permission)))
    # walks through the directory tree
    os_walk(options.root_dir)