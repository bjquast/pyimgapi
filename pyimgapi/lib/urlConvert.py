import pudb
import base64
import re

def url2filename(url):
	filename = url.replace('https://', '').replace('http://', '')
	pattern = (r'[\W]')
	filename = re.sub(pattern, '_', filename)
	return filename
