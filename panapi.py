## API handler for PANW next generation firewall
##
## This is an API handler program for PANW next generation firewall
## to make use API easy.
##

import xml.etree.ElementTree as ET
import httplib
import urllib
import urllib2
import sys
from urllib2 import Request, urlopen, URLError, HTTPError

DEFAULT_PARAMETERS = {'user': 'admin', 'password': 'admin'}

class PANWAPIHandler(object):
	def __init__(self, host, parameters):
		self.session_key = ''
		self._parameters = {}
		self._parameters.update(DEFAULT_PARAMETERS)
		self._parameters.update(parameters)
		
		self._url = 'https://' + host + '/api/'
		self.rawdata_op = ''

	def _urlfetch(self):
		self.postdata = self.parameters
		self.postdata.update(self._parameters)
		if self.session_key:
			self.parameters.update({'key': self.session_key})
			del self.parameters["user"]
			del self.parameters["password"]
			
		try:
			self.data = urllib.urlencode(self.postdata)
			self.request = urllib2.Request(self._url,self.data)
			self.content = urllib2.urlopen(self.request).read()
		except URLError, e:
			if hasattr(e, 'reason'):
				print 'Failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code'):
				print 'The server couldn\'t fulfill the request.'
				print 'Error code: ', e.code
		else:
			try:
				self.response_tree = ET.fromstring(self.content)

			except Exception as ex:
				return self.content

			else:
				return self.response_tree

	def key(self):
		self.parameters = {'type': 'keygen'}
		self.rawdata_key = self._urlfetch()
		self.session_key = self.rawdata_key.find('result/key').text
		return self.session_key

	def op(self,cmd):
		self.cmd = cmd
		self.parameters = {'type': 'op', 'cmd': self.cmd}
		self.rawdata_op = self._urlfetch()
		return self.rawdata_op

	def config(self,action,xpath,element):
		self.action = action
		self.xpath = xpath
		self.element = element
		self.parameters = {'type': 'config', 'action': self.action, 'xpath': self.xpath, 'element': self.element}
		self.rawdata_config = self._urlfetch()
		return self.rawdata_config

	def export(self,params):
		self.parameters = {'type': 'export'}
		self.parameters.update(params)
		self.rawdata_export = self._urlfetch()
		return self.rawdata_export

	def commit(self,cmd):
		self.cmd = cmd
		self.parameters = {'type': 'commit', 'cmd': self.cmd}
		self.rawdata_commit = self._urlfetch()
		if not self.rawdata_commit.get('status') == "success":
				print "fail\n"
				return self.rawdata_commit
		print "success\n"
		return self.rawdata_commit
