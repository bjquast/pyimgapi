import pudb
import pyvips
from tempfile import NamedTemporaryFile




class ImageProcessor():
	def __init__(self, cachedimage):
		self.cachedimage = cachedimage
		self.processed_image = None
		self.loadImage()
		self.saveparams = {'squash': False}
		# initialize targetformat with the current format and change it when a format change is requested
		self.targetfileformat = self.cachedimage.getFileFormat()
		
	
	def loadImage(self):
		self.img = pyvips.Image.new_from_file(self.cachedimage.getFilePath())
	
	def writeImage(self):
		if self.targetfileformat.lower() in ['tif', 'tiff']:
			self.img.tiffsave(self.cachedimage.getTargetFilePath(), squash = self.saveparams['squash'])
			
		elif self.targetfileformat.lower() in ['pgm', 'pnm', 'pbm']:
			self.img.ppmsave(self.cachedimage.getTargetFilePath(), squash = self.saveparams['squash'])
			
		elif self.targetfileformat.lower() in ['png']:
			self.img.pngsave(self.cachedimage.getTargetFilePath())
		
		elif self.targetfileformat.lower() in ['jpeg', 'jpg']:
			self.img.jpegsave(self.cachedimage.getTargetFilePath())
	
	
	def setTargetFileFormat(self, fileformat):
		# only set the targetfileformat attribute
		# will be used later in writeImage()
		self.targetfileformat = fileformat
		
		# ensure that the image data are fitting into the ppm formats if they are choosen
		if self.targetfileformat == 'pbm':
			self.colorMode('bitonal')
		elif self.targetfileformat == 'pgm':
			self.colorMode('gray')
		
	
	def rotateImage(self, angle):
		self.processed_image = self.img.similarity(angle=float(angle))
		self.img = self.processed_image
	
	def colorMode(self, colormode):
		if colormode.lower() == 'gray':
			self.processed_image = self.img.colourspace('b-w')
			self.img = self.processed_image
		elif colormode.lower() == 'bitonal':
			i = self.img.colourspace('b-w')
			self.processed_image = i > 128 # what the f.. https://github.com/libvips/libvips/issues/59
			self.img = self.processed_image
			self.saveparams['squash'] = True
		else:
			pass
		return
	
	def resizeImage(self, factor = None, minwidth = None, minheight = None, maxwidth = None, maxheight = None):
		
		(factor, hfactor) = self.getResizeFactor(factor, minwidth, minheight, maxwidth, maxheight)
		
		if factor is not None:
			if hfactor is not None:
				self.processed_image = self.img.resize(factor, vscale=hfactor)
			else:
				self.processed_image = self.img.resize(factor)
			self.img = self.processed_image
		return
	
	
	def getResizeFactor(self, factor, minwidth, minheight, maxwidth, maxheight):
		# factor is the factor to scale the image size with. When hfactor is set the image will be stretched to the width of factor and the height of hfactor 
		
		currentwidth = self.img.width
		currentheight = self.img.height
		hfactor = None
		
		if factor is not None:
			return (factor, hfactor)
		
		elif minwidth is not None and minheight is not None:
			factor = minwidth / currentwidth
			hfactor = minheight / currentheight
			#if wfactor > hfactor:
			#	factor = wfactor
			#else:
			#	factor = hfactor
		
		elif minwidth is not None:
			factor = minwidth / currentwidth
		
		elif minheight is not None:
			factor = minheight / currentheight
		
		elif maxwidth is not None and maxheight is not None:
			wfactor = maxwidth / currentwidth
			hfactor = maxheight / currentheight
			if wfactor < hfactor:
				factor = wfactor
				hfactor = None
			else:
				factor = hfactor
				hfactor = None
		return factor, hfactor
	
	
	def cropImage(self, croptype = None, cropunit = None, offsetx = None, offsety = None, cropwidth = None, cropheight = None):
		currentwidth = self.img.width
		currentheight = self.img.height
		
		#pudb.set_trace()
		if offsetx == None:
			offsetx = 0
		if offsety == None:
			offsety = 0
		
		if croptype == 'square':
			if currentwidth > currentheight:
				offsetx = int((currentwidth - currentheight) / 2)
				cropwidth = currentheight
				offsety = 0
				cropheight = currentheight
			
			else:
				offsetx = 0
				cropwidth = currentwidth
				offsety = int((currentheight - currentwidth) / 2) 
				cropheight = currentwidth
		
		elif croptype == 'rectangle':
			if cropunit == 'percent':
				if offsetx > 100:
					offsetx = 100
				if offsety > 100:
					offsety = 100
				if cropwidth is None:
					cropwidth = (1 - offsetx / 100) * currentwidth
				else:
					cropwidth = (cropwidth / 100) * currentwidth
				if cropheight is None:
					cropheight = (1 - offsety / 100) * currentheight
				else:
					cropheight = (cropheight / 100) * currentheight
				# offset must be changed after cropwidth and cropheight have been calculated
				offsetx = (offsetx / 100) * currentwidth
				offsety = (offsety / 100) * currentheight
			elif cropunit == 'pixel':
				if cropwidth is None:
					cropwidth = currentwidth - offsetx
				if cropheight is None:
					cropheight = currentheight - offsety
		
		if offsetx >= currentwidth:
			offsetx = currentwidth - 1
		if (offsetx + cropwidth) > currentwidth:
			cropwidth = currentwidth - offsetx
		
		if offsety >= currentheight:
			offsety = currentheight - 1
		if (offsety + cropheight) > currentheight:
			cropheight = currentheight - offsety
		
		if cropwidth <= 0:
			cropwidth = 1
		if cropheight <= 0:
			cropheight = 1
		
		self.processed_image = self.img.crop(offsetx, offsety, cropwidth, cropheight)
		self.img = self.processed_image
		
		return
		
	
	
	def getImageWidth(self):
		return self.img.width
	
	def getImageHeight(self):
		return self.img.height
	
	def getTargetFilePath(self):
		return self.cachedimage.getTargetFilePath()
	
	def getTargetFileFormat(self):
		return self.targetfileformat
	
	
	
	
