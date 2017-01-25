#!/bin/python

# see original script here : https://github.com/dnmellen/pyusbalarm
# getting UUIDs on Ubuntu terminal : $ blkid

import usb
from usb import USBError
import time

ListOfDriveUUIDs = []


class USBDetector(object):
    """ USB Device Detector Class. """

    def __init__(self, devices=None, payload=None, check_interval=0.5):
        """ Constructor

        @param devices:
        @param payload: function to call if any device is connected
        @param check_interval: number of secs to wait in each check
        """

        self.devices = devices or []
        self.payload = payload
        self.check_interval = check_interval

    def get_usb_devices(self):
        """ Return all attached USB devices. """

        return usb.core.find(find_all=True)

    def print_usb_devices(self):
        """ Print info of connected USB devices. """

        for device in self.get_usb_devices():
            print device

    def is_any_connected(self):
        """ Check if any device has been connected. """

        drive_detected = False
        for device in self.get_usb_devices():
            if device.uuid in self.devices:
                drive_detected = True

        return drive_detected

    def run(self):
        """ Continuously check if a device is connected."""

        while True:
            if self.is_any_connected() and self.payload:
                self.payload()
            time.sleep(self.check_interval)


if __name__ == '__main__':
    # Catch signal CTRL+C to exit test
    import signal
    import sys

    def signal_handler(signal, frame):
        print 'You Pressed CTRL+C'
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    detector = USBDetector(devices=ListOfDriveUUIDs)

    print "* Exploring devices *"
    detector.print_usb_devices()
    print "==================="

    print "Monitoring USB devices... (Press CTRL+C for exit)"
#    detector.run()
