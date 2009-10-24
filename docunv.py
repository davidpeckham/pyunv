#!/usr/bin/env python
# encoding: utf-8
"""
docunv.py

Created by David Peckham on 2009-10-24.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import sys
import getopt

from pyunv.universe import Universe
from pyunv.reader import Reader
from pyunv.manifest import Manifest

help_message = '''
Create a text manifest for your BusinessObjects XI R2 universe.

Example:
  docunv universe.unv
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
        
        if len(args) == 0:
            raise Usage(help_message)
            
        verbose = False
        output = None
            
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
        
        universe_filename = args[0]
        reader = None
        try:
            with open(universe_filename, 'rb') as universe_file:
                reader = Reader(universe_file)
                
            if output is None:
                manifest_filename = universe_filename+'.txt'
            else:
                manifest_filename = output
                
            with open(manifest_filename, 'w') as manifest_file:
                Manifest(reader.universe).save(manifest_file)
        except IOError as error:
            print >> sys.stderr, "Unable to open %s: %s (error %d)" % (
                error.filename, error.strerror, error.errno)
            return 1
        except Exception:
            print >> sys.stderr, "Unable to document this universe. Please send the following error message to dave.peckham@me.com"
            raise

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
