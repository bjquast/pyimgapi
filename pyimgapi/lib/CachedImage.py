import pudb
import requests
import os
import time
import re

#from PIL import Image
import pyvips
from tempfile import NamedTemporaryFile 
from .PyImgAPIErrors import ImageFormatNotAccepted

from configparser import ConfigParser
config = ConfigParser()
config.read('./pyimgapi/config.ini')


# from https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un

class CachedImage():
	def __init__(self, imageurl, cachedir, tilesdir):
		self.imageurl = imageurl
		self.cachedir = cachedir
		self.tilesdir = tilesdir
		self.sslverify = config.getboolean('ssl_requests', 'sslverify')
		
		self.user_agent = config.get('request_headers', 'user-agent')
		self.request_headers = {'User-Agent': self.user_agent}
		
		if not os.path.isdir(self.cachedir):
			os.makedirs(self.cachedir)

		if not os.path.isdir(self.tilesdir):
			os.makedirs(self.tilesdir)

		self.createTempFiles()
		self.fetchImageFromURL()
		self.readImageFormat()
		self.setImageInfo()
		
		del self.image
	
	
	
	def createTempFiles(self):
		self.cachedfile = NamedTemporaryFile(dir=self.cachedir)
		self.filepath = self.cachedfile.name
		self.targetcachedfile = NamedTemporaryFile(dir=self.cachedir)
		self.targetfilepath = self.targetcachedfile.name
	
	def fetchImageFromURL(self):
		r = requests.get(self.imageurl, allow_redirects=True, verify=self.sslverify, headers=self.request_headers)
		self.cachedfile.write(r.content)
	
	def readImageFormat(self):
		try:
			self.image = pyvips.Image.new_from_file(self.cachedfile.name)
		except pyvips.error.Error as e:
			raise ImageFormatNotAccepted('Image url does not reference an accepted image format.')
		
		loader = self.image.get('vips-loader')
		self.fileformat = re.sub(r'load$', '', loader)
	
	def setImageInfo(self):
		self.height = self.image.height
		self.width = self.image.width
		#self.palette = image.palette
		
	
	def getFileFormat(self):
		return self.fileformat
	
	def getFilePath(self):
		return self.filepath
	
	def getTargetFilePath(self):
		return self.targetfilepath
	
	def closeTempFiles(self):
		self.cachedfile.close()
		self.targetcachedfile.close()




