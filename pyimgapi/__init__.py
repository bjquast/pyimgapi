from pyramid.config import Configurator
from pyramid.renderers import JSONP


def main(global_config, **settings):
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')
	config.add_renderer('jsonp', JSONP(param_name='callback'))
	
	config.add_route('imageprocessor', '/process')
	
	# ordering of the routes is important here
	config.add_route('iiif_image_url', '/image/{id}/{region}/{size}/{rotation}/{targetfilename}')
	config.add_route('imageprocessor_image', '/image')
	
	config.add_route('imageview', '/view')
	config.add_route('help', '/')
	
	config.add_route('deepzoom', '/deepzoom')
	config.add_route('tiles', '/tilesCache/{imageurl}/{dirnum}/{filename}')
	
	config.add_static_view(name='static', path='pyimgapi:static')
	
	config.scan()
	return config.make_wsgi_app()
