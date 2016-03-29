#!/usr/bin/python

# Python script to delete all C++ source and header files from a root directory

import os,sys,time,datetime,logging
from optparse import OptionParser

FILE_EXTENSIONS=['.h','.cpp']

# -----------------------------------------------------------------------------
def step(ext, dirname, names):
    '''function executed by walk in every new folder'''
    for e in ext:
        e = e.lower()
        for name in names:
            if name.lower().endswith(e):
                file_path = os.path.join(dirname,name)
                logging.info(file_path)
                if not options.dry_run:
                    os.remove(file_path)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    usage = "%prog - Delete all c++ header and source files in a given root directory."
    parser = OptionParser(usage = usage)

    parser.add_option("-d", "--root_directory",
                      action="store", type="string", dest="root_directory",
                      default="")
    parser.add_option("--dry_run", 
                      action="store_true", dest="dry_run", default=False,
                      help='print output without deleting any files')
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
    start_time_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')
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
    if not options.root_directory or not os.path.exists(options.root_directory):
        logging.critical('root directory does not exist: %s', options.root_directory)
        sys.exit(-1)

    # walks through the directory tree, performing the 'step' function at every step  
    os.path.walk(options.root_directory, step, FILE_EXTENSIONS)    
