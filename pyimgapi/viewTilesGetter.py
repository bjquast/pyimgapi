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

import pudb
import json
import time
import os


class TilesGetterView(object):
	def __init__(self, request):
		self.request = request
		self.view_name = "pyimgapi TilesGetter"
		
		self.tilesdir = config.get('tiles_cache', 'dir')


	@view_config(route_name='tiles')
	def tilesgetterview(self):
		
		imageurl = self.request.matchdict['imageurl']
		dirnum = self.request.matchdict['dirnum']
		filename = self.request.matchdict['filename']
		
		filepath = self.tilesdir + '/' + imageurl + '/' + dirnum + '/' + filename
		
		
		if os.path.isfile(filepath):
			response = FileResponse(filepath, content_type='image/' + 'jpeg')
			response.headers['Content-Disposition'] = ("filename={0}".format(filename))
			
			return response
		else:
			return HTTPNotFound()
