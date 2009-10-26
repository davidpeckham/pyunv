#!/usr/bin/env python
# encoding: utf-8
"""
docunv.py

Created by David Peckham on 2009-10-24.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import sys
import getopt

import pyunv
from pyunv.universe import Universe
from pyunv.reader import Reader
from pyunv.manifest import Manifest

__version__ = "0.1.0"

help_message = '''
Create a text manifest for your BusinessObjects XI R2 universe.
Copyright (c) 2009 David Peckham. All rights reserved

pyunv options universe.unv

    where options are:

    -m  --manifest   manifest output file 
    -t  --template   manifest template
    -h  --help       show this help

Examples:
  docunv universe.unv
  docunv --manifest manifest.txt universe.unv 
  docunv --manifest manifest.txt --template manifest.mako universe.unv 
'''

def version():
    return ' %s (pyunv %s)' % (__version__, pyunv.__version__)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hm:t:v", ["help", "manifest=", "template="])
        except getopt.error, msg:
            raise Usage(msg)
        
        if len(args) == 0:
            raise Usage(help_message)
            
        verbose = False
        manifest = None
        template = None
            
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-m", "--manifest"):
                manifest = value
                if manifest.endswith('.unv'):
                    raise Usage(help_message)
            if option in ("-t", "--template"):
                template = value
        
        universe_filename = args[0]
        reader = None
        try:
            with open(universe_filename, 'rb') as universe_file:
                reader = Reader(universe_file)
                
            if manifest is None:
                manifest_filename = universe_filename+'.txt'
            else:
                manifest_filename = manifest
                
            with open(manifest_filename, 'w') as manifest_file:
                Manifest(reader.universe, template).save(manifest_file)
        except IOError as error:
            print >> sys.stderr, "Unable to open %s: %s (error %d)" % (
                error.filename, error.strerror, error.errno)
            return 1
        except Exception:
            print >> sys.stderr, "Unable to document this universe. Please send the following error message to dave.peckham@me.com"
            raise

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + version() +": " + str(err.msg)
        # print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
