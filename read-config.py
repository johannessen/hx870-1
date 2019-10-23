#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, sys, os

import hxtool


def progress_bar(progress):
    sys.stdout.write(".")
    sys.stdout.flush()

class HxToolArgs(object):
    def __init__(self):
        self.model = None
        self.tty = None
        self.simulator = None

def config_read():
    h = hxtool.get(HxToolArgs())
    try:
        if not h.comm.cp_mode:
            raise Exception("not in CP mode (region mismatch?)")
        h.comm.sync()
        mmsi = h.config.read_mmsi()[0]
    except Exception as exc:
        print( "Could not open connection to HX870." )
        sys.exit(1)
    print( "Device MMSI " + (mmsi if mmsi != "ffffffffff" else "not set") )
    sys.stdout.write( "Reading HX870 memory " )
    sys.stdout.flush()
    try:
        h.config.set_progress_callback(progress_bar)
        config = h.config.config_read()
    except Exception as exc:
        print( " Error!" )
        raise exc
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
