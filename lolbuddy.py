#!/usr/bin/python

import sys

if sys.argv[1] in ('--help', '-help', 'help', '-h', '--h'): #Though really if they're typing in anything as a CLI arg, they probably want help
    print(
        '\n\nlolbuddy help:'
        '\n\nUse "lolbuddy" to start lolbuddy'
        '\n\nIf no API key or league installation location have been entered, or they are invalid, you will be prompted for the API key, and lolbuddy will check the default league location for your OS. If it is not found, you will be prompted for that as well.'
        '\n\nexiting...\n'
        )
else:
    main()

def main():
    APIkey = input('API key not found, please enter it: ')
    location = input('League of Legends not found in the default location, please enter its current location: ')
