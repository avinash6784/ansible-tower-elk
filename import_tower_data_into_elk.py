#!/usr/bin/python

import sys, os.path, datetime
import urllib2, urllib, json, base64, argparse, re
from collections import defaultdict

# Elasticsearch python libs
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Tower Cli python libs
import tower_cli
from tower_cli import get_resource
from tower_cli import conf

def main():
    global tower_auth_key
    
    # Process arguments
    parser = argparse.ArgumentParser(description='Process arguments')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    required.add_argument("-H", "--host", type=str, required=True, help="Ansible Tower Hostname")
    required.add_argument("-U", "--username", type=str, required=True, help="Ansible Tower Username")
    required.add_argument("-P", "--password", type=str, required=True, help="Ansible Tower Password")
    optional.add_argument("-T", "--job_type", type=str, required=False, help="Ansible Tower Job Type")
    args = parser.parse_args()
    
    # Invoke tower authentication and import data to elasticsearch
    tower_auth_key = get_tower_auth_key(args.host, args.username, args.password)    
    import_tower_data_into_elk(args.host, args.username, args.password, args.job_type)

if __name__ == '__main__':
    main()
    
