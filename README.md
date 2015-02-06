# opendns_investigate_tool

Helper script for the security office to have easier access to the OpenDNS investigate tool -- eliminates having to remember curl syntax and investigate file paths.

Don't forget to set the 'OPENDNS_API_TOKEN' in your bash environment to your OWN api key.

# Usage:
```
usage: opendns.py [-h] [-i [DOMAIN [DOMAIN ...]]] [-f FILE] [-c CAT] [-o OUTFILE] [-r] [-v] [-d]

helper script to allow easy script access to the OpenDNS investigate API.

optional arguments:
  -h, --help
      show this help message and exit
  -i [DOMAIN [DOMAIN ...]], --investigate [DOMAIN [DOMAIN ...]]
      specify domain to investigate
  -f FILE, --file FILE
      specify file with a list of lookups
  -c CAT, --category CAT
      specify which category to report on
  -o OUTFILE, --outfile OUTFILE
      write results to a file instead of STDOUT
  -r, --readable
      print results in human-readable format
  -v, --verbose
      print with verbose labels
  -d, --debug
      turn on debugging
```
