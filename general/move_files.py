#!/usr/bin/python

# Python script to rename and move files that contain specified strings 

import fnmatch, shutil, os,sys,time,datetime,logging
from optparse import OptionParser

LASER2D="laser2d.monolithic"
LMS="LMS1xx.monolithic"

MIPIMU="MicrostrainMIPIMU.monolithic"
MIPRAW="MicrostrainMIPRawPacketData.monolithic"

ext=[LASER2D, LMS, MIPIMU, MIPRAW]
# -----------------------------------------------------------------------------
def rename_laser_files(root, dirs, files):
    '''function executed by walk in every new folder'''

    os.chdir(root)

    subdir = ""
    for d in dirs:
        subdir = d

    for f in files:
        for e in ext:
            if fnmatch.fnmatch(f, "*"+e) and not fnmatch.fnmatch(f,e):
                logging.info(e + " : " + f)
            
                new_path = os.path.join(root, subdir, e)
                logging.info("...moving to " + new_path)
                if not options.dry_run:
                    shutil.move(os.path.join(root,f), new_path)


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    usage = "%prog - Rename and move files that contain the specified strings."
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

    # walks through the directory tree, performing the given function at every step  
    for root, dirs, files in os.walk(options.root_directory):
        rename_laser_files(root, dirs, files)

    logging.info("Complete")
