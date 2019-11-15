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


class ImageProcessorView(object):

	def __init__(self, request):
		self.request = request
		self.view_name = "Image processing web service"
		
	
	@view_config(route_name='imageprocessor')
	@view_config(route_name='imageprocessor_image')
	def processorview(self):
		# pudb.set_trace()
		requestparams = RequestParameters(self.request)
		requestparams.readRequestParams()
		
		imageurl = requestparams.getImageURL()
		if imageurl is None:
			return HTTPNotFound()
		
		try:
			cachedimage = CachedImage(imageurl)
		except ValueError:
			return HTTPNotFound()
		imageprocessor = ImageProcessor(cachedimage)
		
		
		for process in requestparams.getProcessingOrder():
			if process == 'rotation':
				angle = requestparams.getRotation()
				if angle is not None:
					imageprocessor.rotateImage(angle)
			
			elif process == 'colormode':
				colormode = requestparams.getColorMode()
				if colormode is not None:
					imageprocessor.colorMode(colormode)
			
			elif process == 'resize':
				params = requestparams.getResizeParams()
				if params is not None:
					imageprocessor.resizeImage(params['factor'], params['minwidth'], params['minheight'], params['maxwidth'], params['maxheight'])
			
			elif process == 'crop':
				params = requestparams.getCropParams()
				if params is not None:
					imageprocessor.cropImage(params['croptype'], params['cropunit'], params['offsetx'], params['offsety'], params['cropwidth'], params['cropheight'])
			
			elif process == 'fileformat':
				fileformat = requestparams.getFileFormat()
				if fileformat is not None:
					imageprocessor.setTargetFileFormat(fileformat)
			
		imageprocessor.writeImage()
		
		targetfile = imageprocessor.getTargetFilePath()
		targetfileformat = imageprocessor.getTargetFileFormat()
		
		response = FileResponse(targetfile, content_type='image/' + targetfileformat)
		response.headers['Content-Disposition'] = ("filename={0}.{1}".format('image', targetfileformat))
		
		return response
