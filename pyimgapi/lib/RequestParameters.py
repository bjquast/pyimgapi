import pudb
import pyvips
import re


class RequestParameters():
	def __init__(self, request):
		self.request = request
		self.processingorder = ('crop', 'rotation', 'resize', 'colormode')
		self.rotation = None
		self.colormode = None
		self.fileformat = None
		self.imageurl = None
		
		self.resizeparams = None
		self.minwidth = None
		self.minheight = None
		self.maxwidth = None
		self.maxheight = None
		self.factor = None
		
		self.regionparams = None
		self.croptype = None
		self.cropunit = None
		self.offsetx = None
		self.offsety = None
		self.cropwidth = None
		self.cropheight = None
		
		
		self.known_colormodes = ['gray', 'bitonal', 'color'] #, 'default' does not change the image
		self.known_formats = ['png', 'jpg', 'tiff', 'tif']
	
	
	def readRequestParams(self):
		#convert all parameter keys to lowercase 
		self.paramsdict = {}
		for param in self.request.params:
			try:
				pvalues = self.request.params.getall(param)
			except AttributeError: # -- not a multidict
				pvalues = [self.request.params[param]]
			self.paramsdict[param.lower()] = pvalues
		
		self.readRotation()
		self.readCrop()
		self.readColorMode()
		self.readResize()
		self.readFileFormat()
		self.readImageURL()
	
	
	def readImageURL(self):
		if 'imageurl' in self.paramsdict:
			self.imageurl = self.paramsdict['imageurl'][0]
	
	def readFileFormat(self):
		if 'fileformat' in self.paramsdict:
			if self.paramsdict['fileformat'][0] in self.known_formats:
				self.fileformat = self.paramsdict['fileformat'][0]
	
	def readRotation(self):
		if 'rotation' in self.paramsdict:
			self.rotation = self.paramsdict['rotation'][0]
		elif 'rotate' in self.paramsdict:
			self.rotation = self.paramsdict['rotate'][0]
	
	def readCrop(self):
		if 'crop' in self.paramsdict:
			cropparams = self.paramsdict['crop'][0]
			pattern1 = re.compile(r'(square)', re.I)
			pattern2 = re.compile(r'(pct\:)*(\d+\.*\d*)*\,(\d+\.*\d*)*\,(\d+\.*\d*)*\,(\d+\.*\d*)*', re.I)
			
			m = pattern1.match(cropparams)
			
			if m is not None:
				if m.groups()[0] is not None:
					self.croptype = 'square'
			
			else:
				m = pattern2.match(cropparams)
				if m is not None:
					self.croptype = 'rectangle'
					
					if m.groups()[0] is not None and m.groups()[0].lower() == 'pct:':
						self.cropunit = 'percent'
						
					elif m.groups()[0] is None:
						self.cropunit = 'pixel'
					
					try:
						self.offsetx = float(m.groups()[1])
					except TypeError:
						self.offsetx = None
					try:
						self.offsety = float(m.groups()[2])
					except TypeError:
						self.offsety = None
					try:
						self.cropwidth = float(m.groups()[3])
					except TypeError:
						self.cropwidth = None
					try:
						self.cropheight = float(m.groups()[4])
					except TypeError:
						self.cropheight = None
			
			self.regionparams =  {'croptype': self.croptype, 'cropunit': self.cropunit, 'offsetx': self.offsetx, 'offsety': self.offsety, 'cropwidth': self.cropwidth, 'cropheight': self.cropheight}
	
	
	def readColorMode(self):
		if 'colormode' in self.paramsdict:
			if self.paramsdict['colormode'][0].lower() in self.known_colormodes:
				self.colormode = self.paramsdict['colormode'][0]
	
	def readResize(self):
		resizeparams = None
		
		if 'resize' in self.paramsdict:
			resizeparams = self.paramsdict['resize'][0]
		
		elif 'size' in self.paramsdict:
			resizeparams = self.paramsdict['size'][0]
		
		if resizeparams is not None:

			pattern1 = re.compile(r'(pct)\:(\d+\.*\d*)', re.I)
			pattern2 = re.compile(r'(\!)*(\d+\.*\d*)*\,(\d+\.*\d*)*')
			
			m = pattern1.match(resizeparams)
			if m is not None:
				if m.groups()[1] is not None:
					self.factor = 0.01 * float(m.groups()[1])
			else:
				m = pattern2.match(resizeparams)
				if m is not None:
					if m.groups()[0] == '!':
						try:
							self.maxwidth = m.groups()[1]
							self.maxheight = m.groups()[2]
						except IndexError:
							self.factor = None
					
					if m.groups()[0] != '!':
						try:
							self.minwidth = m.groups()[1]
							self.minheight = m.groups()[2]
						except IndexError:
							factor = None
					
					if self.maxwidth is not None:
						self.maxwidth = float(self.maxwidth)
					if self.maxheight is not None:
						self.maxheight = float(self.maxheight)
					if self.minwidth is not None:
						self.minwidth = float(self.minwidth)
					if self.minheight is not None:
						self.minheight = float(self.minheight)
		
			self.resizeparams = {'factor': self.factor, 'minwidth': self.minwidth, 'minheight': self.minheight, 'maxwidth': self.maxwidth, 'maxheight': self.maxheight}
	
	
	def getImageURL(self):
		return self.imageurl
	
	def getFileFormat(self):
		return self.fileformat
	
	def getRotation(self):
		return self.rotation
	
	def getCropParams(self):
		return self.regionparams
	
	def getColorMode(self):
		return self.colormode
	
	def getResizeParams(self):
		return self.resizeparams
	
	def getProcessingOrder(self):
		return self.processingorder
	