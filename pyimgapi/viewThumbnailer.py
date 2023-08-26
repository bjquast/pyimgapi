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


'''
this is a stub to start development on a thumbnailer

# code from gbol portal for pdf thumbnails of the first page

import subprocess


try:
	callresult = subprocess.check_output(["convert", '-thumbnail', '190x270!', '-flatten', filePath + "[0]", thumbpath], timeout=50)
except Exception as e:
	self.message1 = "\nCan not generate thumbnail: {0}".format(e)
	filename = ''
	thumbfile = ''


'''
