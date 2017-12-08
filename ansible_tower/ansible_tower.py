#!/usr/bin/python

import sys, os.path, datetime
import urllib2, urllib, json, base64

# Ansible tower_cli python libs
import tower_cli
from tower_cli import get_resources
from tower_cli import conf

class AnsibleTower:

	def __init__(self, host, username, password):
		''' Constructor for this class. '''
		self.host = host
		self.username = username
		self.password = password

	# Authenticate to Tower API and get API auth key/token
	def auth_token(self):
		try:
			req = urllib2.Request(
				url = 'https://' + self.host + '/api/v1/authtoken/',
				headers = {
					"Content-Type": "application/json"
				},
				data = json.dumps({
					"username": self.username,
					"password": self.password
				})
			)
			response = urllib2.urlopen(req)
			results = json.loads(response.read())
			self.token = results['token']
		except urllib2.URLError as error:
			module.fail_json(msg='Unable to retrieve Tower Auth Key due to error : {0} '. format(error))

	# Get tower organizations
	def organizations(self, org_id = None):
		try:
			if org_id != None:
				req = urllib2.Request(
					url = 'https://' + self.host + '/api/v1/organizations/' + org_id + '/',
					headers = {
						"Content-Type": "application/json",
						"Authorization": "Token " + self.token
					}
				)
				response = urllib2.urlopen(req)
				results = json.loads(response.read())
			else:
				with conf.settings.runtime_values(host=self.host, username=self.username, password=self.password):
					res = tower_cli.get_resource('organization')
					results = res.list(all_pages=True)

			return results
		except urllib2.URLError as error:
			module.fail_json(msg='Unable to retrieve Tower Organizations due to error : {0} '. format(error))
			
	# Get tower projects
	def projects(self, project_id = None):
		try:
			if project_id != None:
				req = urllib2.Request(
					url = 'https://' + self.host + '/api/v1/projects/' + str(project_id) + '/',
					headers = {
						"Content-Type": "application/json",
						"Authorization": "Token " + self.token
					}
				)
				response = urllib2.urlopen(req)
				results = json.loads(response.read())
			else:
				with conf.settings.runtime_values(host=self.host, username=self.username, password=self.password):
					res = tower_cli.get_resource('project')
					results = res.list(all_pages=True)

			return results
		except urllib2.URLError as error:
			module.fail_json(msg='Unable to retrieve Tower Projects due to error : {0} '. format(error))


	# Get tower inventories
	def inventories(self, inventory_id = None):
		try:
			if inventory_id != None:
				req = urllib2.Request(
					url = 'https://' + self.host + '/api/v1/inventories/' + str(inventory_id) + '/',
					headers = {
						"Content-Type": "application/json",
						"Authorization": "Token " + self.token
					}
				)
				response = urllib2.urlopen(req)
				results = json.loads(response.read())
			else:
				with conf.settings.runtime_values(host=self.host, username=self.username, password=self.password):
					res = tower_cli.get_resource('inventory')
					results = res.list(all_pages=True)

			return results
		except urllib2.URLError as error:
			module.fail_json(msg='Unable to retrieve Tower Inventories due to error : {0} '. format(error))
			
	# Get tower data from all resources based on resources type
	def get_resources(self, type = 'job'):
		with conf.settings.runtime_values(host=self.host, username=self.username, password=self.password):
			res = tower_cli.get_resource(type)
			results = res.list(all_pages=True)
		
		return results
