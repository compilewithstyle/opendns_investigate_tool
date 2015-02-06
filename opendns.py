#!/usr/bin/env python

#----------------------------------------------------------------------
#   **Author:
#       Nicholas Siow | n.siow@wustl.edu
#   **Description:
#       helper script to allow easy script access to the
#       OpenDNS investigate API
#   **Revision history:
#       2015_1_23 :: started script
#   **Todo:
#       -
#----------------------------------------------------------------------

import os
import sys
import json
import requests
import argparse

#----------------------------------------------------------------------
# debugging helper functions
#----------------------------------------------------------------------

args = None
def debug( msg ):
    if args.debug:
        print ">DEBUG: {}".format(msg)

def error( msg ):
    print ">>ERROR: {}".format(msg)
    exit(1)

def pretty( string ):
    if args.readable:
        return json.dumps(string, sort_keys=True, indent=4, separators=(',', ': '))
    else:
        return json.dumps( string )

#----------------------------------------------------------------------
# process arguments
#----------------------------------------------------------------------

parser = argparse.ArgumentParser(description=\
'helper script to allow easy script access to the OpenDNS investigate API.')
parser.add_argument('-i', '--investigate', metavar='DOMAIN', nargs='*', help='specify domain to investigate')
parser.add_argument('-f', '--file', help='specify file with a list of lookups')
parser.add_argument('-c', '--category', metavar='CAT', help='specify which category to report on')
parser.add_argument('-o', '--outfile', help='write results to a file instead of STDOUT')
parser.add_argument('-r', '--readable', action='store_true', help='print results in human-readable format')
parser.add_argument('-v', '--verbose', action='store_true', help='print with verbose labels')
parser.add_argument('-d', '--debug', action='store_true', help='turn on debugging')
args = parser.parse_args()

if args.file and args.investigate:
    error("Please use EITHER the -i or -f flag. Run './opendns.py -h' for help.")

if not args.file and not args.investigate:
    error("Please specify either the -i or -f option. Run './opendns.py -h' for help")

if not args.category:
    debug( "no category specified, defaulting to 'domains/score'" )
    args.category = 'domains/score'

OUTSTREAM = None
if args.outfile:
    OUTSTREAM = open( args.outfile, 'w' )
else:
    OUTSTREAM = sys.stdout

#----------------------------------------------------------------------
# script classes and subroutines
#----------------------------------------------------------------------

class Investigator(object):
    """class to help with submitting investigate requests"""

    def __init__( self, token ):
        self.opendns_root = "https://investigate.api.opendns.com/"

        self.categories = [
            "domains/categorization",
            "domains/score",
            "recommendations/name",
            "links/name",
            "security/name",
        ]

        self.headers = {
            'Authorization': 'Bearer ' + token
        }

        debug("using headers: {}".format(self.headers))

    def investigate( self, data, cat ):

        debug("investigate called with the following arguments:")
        debug("\tdata: {}".format(data))
        debug("\tcategory: {}".format(cat))
        
        # make sure that a valid OpenDNS investigate category was requested
        if cat != "all" and cat not in self.categories:
            error("Invalid category: " + cat)

        # if all categories are requested, iterate through the category list
        # and recursively call this function
        elif cat == "all":
            debug("all categories requested, starting iteration now...")
            for c in self.categories:
                self.investigate( data, c )
            return

        # convert the data into the proper format
        if not isinstance(data, list):
            data = [data]
        json_data = json.dumps(data)

        # switch action based on which category of lookup was requested
        if cat in ['domains/categorization', 'domains/score']:

            debug("starting request: " + self.opendns_root+cat+"/")
            r = requests.post( self.opendns_root+cat+"/", data=json_data, headers=self.headers )
            debug("received response: " + r.text)

            if args.verbose:
                print >>OUTSTREAM, "<{}> for {}".format(cat, json_data)
            print >>OUTSTREAM, pretty(json.loads(r.text))

        elif cat in ['recommendations/name', 'links/name', 'security/name']:

            if not isinstance(data, list):
                data = [data]

            results = []
            for d in data:
                debug("starting request: " + self.opendns_root+cat+"/")
                r = requests.get( self.opendns_root+cat+"/{}.json".format(d), headers=self.headers )
                debug("received response: " + r.text)
                results.append(json.loads(r.text))

            if args.verbose:
                print >>OUTSTREAM, "<{}> for {}".format(cat, json_data)
            print >>OUTSTREAM, pretty(r.text)


#----------------------------------------------------------------------
# fetch the API token from environment variables
#----------------------------------------------------------------------

if 'OPENDNS_API_TOKEN' not in os.environ:
    error("No API token found in env variable: OPENDNS_API_TOKEN")

TOKEN = os.environ['OPENDNS_API_TOKEN']
debug("found API token: " + TOKEN)

#----------------------------------------------------------------------
# investigate the specified domain(s)
#----------------------------------------------------------------------

i = Investigator(TOKEN)

if args.investigate:
    domain = args.investigate
    i.investigate( domain, args.category )
elif args.file:
    if os.path.isfile(args.file):
        domains = open(args.file, 'r').read().splitlines()
        for d in domains:
            i.investigate(d, args.category )
    else:
        error("invalid file given: " + args.file)
else:
    error("Something went wrong...")

