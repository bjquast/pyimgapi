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


from configparser import ConfigParser
config = ConfigParser()
config.read('./pyimgapi/config.ini')



class IIIFCanonicalURLView():
	def __init__(self, request):
		self.request = request
		self.view_name = "IIIF compatible image processing web service"
		self.known_formats = [fm.strip() for fm in config.get('images', 'known_formats').split(',')]
		self.known_colormodes = [cm.strip() for cm in config.get('images', 'known_colormodes').split(',')]
		
		self.region = None
		self.size = None
		self.rotation = None
		self.colormode = None
		self.fileformat = None
	
	
	
	
	@view_config(route_name='iiif_image_url')
	def iiifImageURLView(self):
		if 'id' in self.request.matchdict:
			self.region = self.request.matchdict['id']
		
		if 'region' in self.request.matchdict:
			self.region = self.request.matchdict['region']
		
		if 'size' in self.request.matchdict:
			self.size = self.request.matchdict['size']
		
		if 'rotation' in self.request.matchdict:
			self.rotation = self.request.matchdict['rotation']
		
		if 'quality' in self.request.matchdict:
			self.quality = self.request.matchdict['quality']
		
		if 'targetfilename' in  self.request.matchdict:
			targetfilename = self.request.matchdict['targetfilename']
		
		
		self.fileformat = self.getFormatByExtension(targetfilename)
		
		return HTTPNotFound()
		
		
	
	
	
	
	
	
	def getFormatByExtension(self, filename):
		extpattern = '(\.' + '|\.'.join(self.known_formats) + ')$'
		pattern = re.compile(extpattern, re.I)
		m = pattern.search(filename[-1])
		if m is not None:
			extension = m.group()
			return extension
		return None

