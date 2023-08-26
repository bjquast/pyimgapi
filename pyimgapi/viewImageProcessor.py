import logging
log = logging.getLogger(__name__)

from pyramid.response import Response
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.view import (view_config, view_defaults)
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPSeeOther, HTTPUnsupportedMediaType, exception_response
from configparser import ConfigParser

import pudb
import json
import os
import time

config = ConfigParser()
config.read('./pyimgapi/config.ini')

from .lib.ImageProcessor import ImageProcessor
from .lib.PyImgAPIErrors import ImageFormatNotAccepted
from .lib.RequestParameters import RequestParameters
from .lib.CachedImage import CachedImage
from .lib.DomainCheck import DomainCheck

from .lib.urlConvert import url2filename
from .lib.dzi2json import dzi2json


class ImageProcessorView(object):

	def __init__(self, request):
		self.request = request
		self.view_name = "Image processing web service"
		
		self.cachedir = config.get('image_cache', 'cache_dir')
		self.tilesdir = config.get('tiles_cache', 'dir')
		self.max_sleep_time = 10
	
	
	@view_config(route_name='imageprocessor')
	@view_config(route_name='imageprocessor_image')
	def processorview(self):
		self.requestparams = RequestParameters(self.request)
		self.requestparams.readRequestParams()
		
		imageurl = self.requestparams.getImageURL()
		if imageurl is None:
			return HTTPNotFound()
		
		domaincheck = DomainCheck(imageurl)
		if domaincheck.isAllowedDomain() is False:
			raise exception_response(403, detail='Domain of image url is not allowed')
		
		try:
			cachedimage = CachedImage(imageurl, self.cachedir, self.tilesdir)
		except ImageFormatNotAccepted as e:
			return HTTPUnsupportedMediaType(detail=e)
		self.imageprocessor = ImageProcessor(cachedimage)
		self.run_processings()
		
		self.imageprocessor.writeImage()
		
		targetfile = self.imageprocessor.getTargetFilePath()
		targetfileformat = self.imageprocessor.getTargetFileFormat()
		
		response = FileResponse(targetfile, content_type='image/' + targetfileformat)
		response.headers['Content-Disposition'] = ("filename={0}.{1}".format('image', targetfileformat))
		
		cachedimage.closeTempFiles()
		return response


	@view_config(route_name='deepzoom', renderer='jsonp')
	def deepzoomprocessorview(self):
		self.requestparams = RequestParameters(self.request)
		self.requestparams.readRequestParams()
		
		imageurl = self.requestparams.getImageURL()
		if imageurl is None:
			return HTTPNotFound()
		
		domaincheck = DomainCheck(imageurl)
		if domaincheck.isAllowedDomain() is False:
			raise exception_response(403, detail='Domain of image url is not allowed')
		
		jsondict = {}
		
		processstring = ''
		processlist = self.requestparams.getProcessParamsList()
		if len(processlist) > 0:
			processstring = '_' + '_'.join(processlist)
		
		urlfilename = url2filename(imageurl + processstring)
		tempfilepath = None
		
		dzipath = self.tilesdir + '/' + urlfilename
		dzifile = self.tilesdir + '/' + urlfilename + '.dzi'
		dzimarker = self.tilesdir + '/' + urlfilename + '.dzi.part'
		
		if os.path.isfile(dzimarker):
			count = 0
			while count <= self.max_sleep_time:
				if os.path.isfile(dzifile):
					jsondict = dzi2json(dzifile)
					if 'Format' in jsondict:
						break
				time.sleep(1)
				count += 1
		
		elif os.path.isfile(dzifile):
			jsondict = dzi2json(dzifile)
		
		else:
			fd = open(dzimarker, 'w')
			fd.close()
			
			try:
				cachedimage = CachedImage(imageurl, self.cachedir, self.tilesdir)
			except ImageFormatNotAccepted as e:
				return HTTPUnsupportedMediaType(detail=e)
			self.imageprocessor = ImageProcessor(cachedimage)
			self.run_processings()
			
			self.imageprocessor.writeTiles(dzipath)
			
			jsondict = dzi2json(os.getcwd() + '/' + dzifile)
			
			cachedimage.closeTempFiles()
		
		if os.path.isfile(dzimarker):
			os.remove(dzimarker)
		
		jsondict['Url'] = self.request.application_url + '/tilesCache/' + urlfilename + '_files/'
		
		return jsondict





	def run_processings(self):
		for process in self.requestparams.getProcessingOrder():
			if process == 'rotation':
				angle = self.requestparams.getRotation()
				if angle is not None:
					self.imageprocessor.rotateImage(angle)
			
			elif process == 'colormode':
				colormode = self.requestparams.getColorMode()
				if colormode is not None:
					self.imageprocessor.colorMode(colormode)
			
			elif process == 'resize':
				params = self.requestparams.getResizeParams()
				if params is not None:
					self.imageprocessor.resizeImage(params['factor'], params['minwidth'], params['minheight'], params['maxwidth'], params['maxheight'])
			
			elif process == 'crop':
				params = self.requestparams.getCropParams()
				if params is not None:
					self.imageprocessor.cropImage(params['croptype'], params['cropunit'], params['offsetx'], params['offsety'], params['cropwidth'], params['cropheight'])
			
			elif process == 'fileformat':
				fileformat = self.requestparams.getFileFormat()
				if fileformat is not None:
					self.imageprocessor.setTargetFileFormat(fileformat)
		return
