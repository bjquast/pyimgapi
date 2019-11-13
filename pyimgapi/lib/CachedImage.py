import pudb
import requests
import os
import time
from PIL import Image
from tempfile import NamedTemporaryFile 

from configparser import ConfigParser
config = ConfigParser()
config.read('./pyimgapi/config.ini')


# from https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un

class CachedImage():
	def __init__(self, imageurl = None):
		self.imageurl = imageurl
		self.known_formats = [fm.strip() for fm in config.get('images', 'known_formats').split(',')]
		self.cachedir = config.get('image_cache', 'cache_dir')
		
		if self.imageurl is None:
			raise ValueError('class ImageCache: no image url provided')
		
		self.fileformat = self.readFileFormat()
		if self.fileformat is None:
			raise ValueError('class ImageCache: image url does not reference an image')
		
		
		self.createTempFiles()
		self.fetchImageFromURL()
		self.readImage()
		self.setImageInfo()
		self.image.close()
	
	
	
	def createTempFiles(self):
		self.cachedfile = NamedTemporaryFile(dir=self.cachedir)
		self.filepath = self.cachedfile.name
		self.targetcachedfile = NamedTemporaryFile(dir=self.cachedir)
		self.targetfilepath = self.targetcachedfile.name
	
	def fetchImageFromURL(self):
		r = requests.get(self.imageurl, allow_redirects=True)
		self.cachedfile.write(r.content)
	
	def readFileFormat(self):
		h = requests.head(self.imageurl, allow_redirects=True)
		header = h.headers
		contenttype = header.get('content-type')
		
		for fileformat in self.known_formats:
			if fileformat in contenttype.lower():
				self.extension = fileformat
				return fileformat
		
		return None
	
	def readImage(self):
		self.image = Image.open(self.cachedfile.name)
		if self.image.format.lower() not in self.known_formats:
			raise ValueError('class ImageCache: image url does not reference an accepted image format')
	
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
	



