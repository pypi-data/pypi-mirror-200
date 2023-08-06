import os
import sys
import argparse
import datetime
from importlib_metadata import version
import warnings

from gapi.utils import generate_token

warnings.filterwarnings("ignore")
v = version('gapi')
today = datetime.date.today()
year = today.strftime("%Y")

def main():

    program_descripton = f'''
                    _ 
                   (_)
   __ _  __ _ _ __  _ 
  / _` |/ _` | '_ \| |
 | (_| | (_| | |_) | |
  \__, |\__,_| .__/|_|
   __/ |     | |      
  |___/      |_|      
          
GSheet Applications Programming Interface - v{v}
Created by Shahil
Copyright {year}. All rights reserved.
    '''
    parser = argparse.ArgumentParser(description=program_descripton,formatter_class=argparse.RawTextHelpFormatter, add_help=True, usage='python -m gapi -m generate_token -c <cred file path> -t <path to create token.json>')
    parser.add_argument('-m', '--mode', dest='set mode', type=str, help='gapi modes: generate_token', metavar='')
    parser.add_argument('-c', '--creds', dest='credentials file', type=str, help='gsheet cred file', metavar='')
    parser.add_argument('-t', '--token', dest='token file', type=str, help='gsheet token file', metavar='')

    args = parser.parse_args()

    if (args.mode).lower()=='generate_token':
        if os.path.isfile(args.creds):
            generate_token(args.creds,args.token)
        else:
            print('[+] Please provide correct client_secret.json file')
            exit()
    else:
        print('[+] Under Construction!')
        exit()


if __name__=="__main__":
    main()