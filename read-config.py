#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, sys, os

import pyhx870


def progress_bar(progress):
    sys.stdout.write(".")
    sys.stdout.flush()

def config_read():
    try:
        h = pyhx870.get()
        h.init()
        h.sync()
    except Exception as exc:
        print( "Could not open connection to HX870." )
        sys.exit(1)
    mmsi = h.read_mmsi()[0]
    print( "Device MMSI " + (mmsi if mmsi != "ffffffffff" else "not set") )
    sys.stdout.write( "Reading HX870 memory " )
    sys.stdout.flush()
    h.set_progress_callback(progress_bar)
    config = h.config_read()
    print( " done" )
    return config

def main():
    if not len(sys.argv) == 2:
        sys.stderr.write("Usage:\n    %s <file_name>\n" % os.path.basename(sys.argv[0]))
        sys.exit(1)
    filename = sys.argv[1]
    try:
        config = config_read()
    except KeyboardInterrupt:
        print( "\nAborted. File '" + filename + "' unchanged." )
        sys.exit(1)
    with open(filename, "wb") as f:
        f.write(config)


main()
