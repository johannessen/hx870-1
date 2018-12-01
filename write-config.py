#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, sys, os

import pyhx870


def progress_bar(progress):
    sys.stdout.write(".")
    sys.stdout.flush()

def config_write(config):
    try:
        h = pyhx870.get()
        h.init()
        h.sync()
    except Exception as exc:
        print( "Could not open connection to HX870." )
        sys.exit(1)
    print( "Firmware " + h.get_firmware_version() + " installed on device" )
    sys.stdout.write( "Writing to HX870 memory " )
    sys.stdout.flush()
    h.set_progress_callback(progress_bar)
    h.config_write(config)
    print( " done" )


def main():
    if not len(sys.argv) == 2:
        sys.stderr.write("Usage:\n    %s <file_name>\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        config = f.read()
    try:
        config_write(config)
    except KeyboardInterrupt:
        print( "\nAborted. Warning: The device may be in an inconsistent state." )
        sys.exit(1)


main()
