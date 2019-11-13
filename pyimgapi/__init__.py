# package

#from pyramid.authentication import AuthTktAuthenticationPolicy
#from pyramid.authorization import ACLAuthorizationPolicy
#from .security import groupfinder


from pyramid.config import Configurator

def main(global_config, **settings):
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')
	
	config.add_route('imageprocessor', '/process')
	
	config.add_route('iiif_image_url', '/image/{id}/{region}/{size}/{rotation}/{quality}/{targetfilename}')
	config.add_route('imageprocessor_image', '/image')
	
	config.add_route('imageview', '/view')
	config.add_route('help', '/')
	
	
	
	#config.add_route('deepzoom', '/deepzoom/')
	

	
	config.add_static_view(name='static', path='pyimgapi:static')
	# ordering of the routes is important here
	
	config.scan()
	return config.make_wsgi_app()
