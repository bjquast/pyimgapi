import logging
log = logging.getLogger(__name__)

from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.view import (view_config, view_defaults)
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPSeeOther
from configparser import ConfigParser
config = ConfigParser()
config.read('./pyimgapi/config.ini')

from .lib.ImageProcessor import ImageProcessor
from .lib.RequestParameters import RequestParameters
from .lib.CachedImage import CachedImage



import pudb
import json
import re

import urllib.parse


from configparser import ConfigParser
config = ConfigParser()
config.read('./pyimgapi/config.ini')



class IIIFCanonicalURLView():
	def __init__(self, request):
		self.request = request
		self.view_name = "IIIF compatible image processing web service"
		self.known_formats = [fm.strip() for fm in config.get('images', 'known_formats').split(',')]
		self.known_colormodes = [cm.strip() for cm in config.get('images', 'known_colormodes').split(',')]
		
		#self.imageurl = None
		#self.region = None
		#self.size = None
		#self.rotation = None
		#self.colormode = None
		#self.fileformat = None
		self.requestparams = {
				'region': 'full',
				'size': 'pct:100',
				'rotation': '0',
				'quality': 'color',
				'targetfilename': 'image',
				'fileformat': 'jpg'
			}
	
	
	
	@view_config(route_name='iiif_image_url')
	def iiifImageURLView(self):
		pudb.set_trace()
		# first check if i can get an imageurl from path or from id and an url pattern in config.ini
		if 'id' in self.request.matchdict:
			self.imageid = self.request.matchdict['id']
			imageurl = self.getURLFromID()
			if imageurl is not None:
				self.requestparams['imageurl'] = imageurl
			else:
				# TODO: replace with an error message (HTTPError()?)
				return HTTPNotFound()
		
		if 'region' in self.request.matchdict:
			#self.region = self.request.matchdict['region']
			self.requestparams['region'] = self.request.matchdict['region']
		
		if 'size' in self.request.matchdict:
			#self.size = self.request.matchdict['size']
			self.requestparams['size'] = self.request.matchdict['size']
		
		if 'rotation' in self.request.matchdict:
			#self.rotation = self.request.matchdict['rotation']
			self.requestparams['rotation'] = self.request.matchdict['rotation']
		
		if 'quality' in self.request.matchdict:
			#self.quality = self.request.matchdict['quality']
			self.requestparams['quality'] = self.request.matchdict['quality']
		
		if 'targetfilename' in self.request.matchdict:
			#targetfilename = self.request.matchdict['targetfilename']
			self.requestparams['targetfilename'] = self.request.matchdict['targetfilename']
			
			fileformat = self.getFormatByExtension(self.requestparams['targetfilename'])
			if fileformat is not None:
				self.requestparams['fileformat'] = fileformat
		
		paramsstring = urllib.parse.urlencode(self.requestparams, encoding='utf-8')
		url = self.request.application_url + '/process'
		if paramsstring != '':
			url = url + '?' + paramsstring
		
		return HTTPFound(location = url)
		
		
	
	def getURLFromID(self):
		# this does not work because pryamid decodes the url parts in the path on the fly, no idea how to prevent that
		# and if it would help
		#url = urlparse(self.imageid)
		#if url.scheme != '':
		#	if url.netloc != '':
		#		if url.path != '':
		#			imageurl = url.geturl()
		#			return imageurl
		
		urlpattern = config.get('image_server', 'url_pattern')
		
		imageurl = urlpattern.replace('{id}', self.imageid)
		return imageurl
	
	
	
	def getFormatByExtension(self, filename):
		extpattern = '(\.' + '|\.'.join(self.known_formats) + ')$'
		pattern = re.compile(extpattern, re.I)
		m = pattern.search(filename)
		if m is not None:
			extension = m.group()
			return extension
		return None

