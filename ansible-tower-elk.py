#!/usr/bin/python

import sys, os.path, datetime
import argparse, re
from collections import defaultdict

# Elasticsearch python libs
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Ansible Tower python libs
from ansible_tower import AnsibleTower

# Get all tower resources data i.e. jobs, inventory, orgs, projects

def get_tower_data(job_type):
	es_host = 'elk.local.com'
	es_index = 'ansible_tower_' + job_type
	es_type = job_type
	es_user = 'elastic'
	es_password = 'password'
	
	# Get data for asked job_type resources
	events = tower.get_resources(job_type)
	
	# Elasticsearch connection
	es = Elasticsearch([es_host], http_auth=(es_user, es_password))
	
	# Elasticsearch bulk api loop
	if events['count'] > 0:
		bulk_action = []
		for e in events['results']:
			bulk = {
				"_index"  : es_index,
				"_type"   : es_type,
				"_id"     : e['id'],
				"_source" : e,
				}
			bulk_action.append(bulk)
		
		try:
			helpers.bulk(es, bulk_action)
			print 'Imported tower resource data successfully!!!'
		except Exception as ex:
			print 'Error:', ex

def main():
    global tower
    
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
    tower = AnsibleTower(args.host, args.username, args.password)    
    tower.auth_token()
    get_tower_data(args.job_type)

if __name__ == '__main__':
    main()
