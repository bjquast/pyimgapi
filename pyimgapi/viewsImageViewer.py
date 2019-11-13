import logging
log = logging.getLogger(__name__)

from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import (view_config, view_defaults)
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPSeeOther
from configparser import ConfigParser
config = ConfigParser()


from .lib.ImageProcessor import ImageProcessor
from .lib.RequestParameters import RequestParameters



import pudb
import json


class ImageViews(object):

	def __init__(self, request):
		self.request = request
		self.view_name = 'Python Vips Image Processing Service'
		
	
	@view_config(route_name='imageview', accept='text/html')
	def imageview(self):
		requestparams = RequestParameters(self.request)
		requestparams.readRequestParams()
		
		
		

		return HTTPNotFound()
