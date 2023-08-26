# pyimgapi
A webservice for image processing with libvips. The webservice fetches images from URLs and performs basic image processing on the image.  It also implements a IIIF Image API that relies on a given image server as data provider for the service. A DeepZoom-Service for generating tiles pyramids is also inmregrated in the API

## Installation

### Requierements:

  - python >= 3.8
  - libvips (e. g. libvips42 libvips-devel libvips-tools on Ubuntu)


#### 1. Create Virtual Environment

    python3 -m venv ./pyimgapi

#### 2. Download pyimgapi

    cd pyimgapi
    git clone https://github.com/bjquast/pyimgapi.git

#### 3. Setup

    cd pyimgapi
    source ../bin/activate
    python setup.py develop
  
#### 4. Configuration

Copy the example file .pyimgapi/config.txt to .pyimgapi/config.ini

Edit ./pyimgapi/config.ini to match your requirements:


    # a whitelist will exclude all domains not contained in it. When no whitelist is given, 
    # all domains except for the blacklisted are allowed
    [allowed_domains]
    whitelist = localhost, upload.wikimedia.org
    blacklist = 
    
    # temp dir for image processing, files are deleted imediately after processing
    [image_cache]
    cache_dir = ./image_cache

    # directory where tiles for deepzoom are stored, the resulting dirs and files are kept as long as you do not delete them
    [tiles_cache]
    dir = ./tilescache

    [ssl_requests]
    sslverify = True

    # a header for requests to wikimedia to identify you as not being a robot or harvesting machine
    [request_headers]
    user-agent = pyimgapi (https://example.org; mail@example.org)

    [images]
    known_formats = bmp, png, jpg, jpeg, tiff, tif, pnm, pgm, pbm, jp2, jp2k, pdf
    known_colormodes = gray, bitonal, color

    # image server for canonical III image api
    # this service requires, that an url for the images on the server is given and that the last path component
    # marked as {id} here is the identifier for a single image. Keep the {id} in the url_pattern
    [image_server]
    url_pattern = https://example.org/path_to_images/{id}


#### 5 Configure a webserver

By default **production.ini** defines a subpath to your domain (**url_prefix**) and the https protocol (**url_scheme**):

    [server:main]
    use = egg:waitress#main
    port = 6549
    url_scheme = https
    url_prefix = /pyimgapi


To use the API in production you can set up a proxy in your webserver that redirects from https://yourdomain/pyimgapi to http://localhost:6549/pyimgapi.

The pyimgapi has no authentication mechanism yet, but the basic authentication by the web server can be used. It is recommended to allow https-connections only in order to keep the password secret. Here is an example for the Apache2 webserver:


    # example with snakeoil certificate, adapt to your needs
    # The pyimgapi is configured to work on https protocol. Settings in development.ini and production.ini
    <virtualhost *:443>
        SSLEngine On
        SSLCipherSuite HIGH:MEDIUM
        SSLCertificateFile /etc/ssl/certs/ssl-cert-snakeoil.pem
        SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
        DocumentRoot /var/www/html
        ServerAdmin mail@example.com
    [...]
    
    
        # basic auth for pyimgapi as it does not has any authentication / authorization mechanism yet
        <Location /pyimgapi>
            AuthType Basic
            AuthName pyimgapi
            Require valid-user
            AuthUserFile /etc/apache2/pyimgapi_passwd
        </Location>
    
    [...]

    #Proxy for pyimgapi:
    ProxyPass /pyimgapi http://localhost:6549/pyimgapi connectiontimeout=5 timeout=300
    ProxyPassReverse /pyimgapi http://localhost:6549/pyimgapi
    ProxyPreserveHost On
    ProxyRequests Off

    [...]
    
    </virtualhost>

Set a user and password on your server with:

    sudo htpasswd -c /etc/apache2/pyimgapi_passwd username



The configuration in **development.ini** allows you to use the API with the url **http://localhost:6549** for testing and development without any special configuration of your webserver.

#### 6 Start the Webservice

The API is started with:

    pserve production.ini

or

    pserve development.ini

#### 7 Usage

https://yourdomain.com/pyimgapi/ or http://localhost:6549/ will show you an example page with typical requests to the image api. The following path components are available:

https://yourdomain.com/pyimgapi/process?

will do the requested image processing on a image fetched from **imageurl=**. You can use parameters like: **rotate=**, **resize=**, **crop=**. Hints how to use them are given on the example page in the root path https://yourdomain.com/pyimgapi/

A request to the API like:

    https://yourdomain.com/pyimgapi/process?rotate=8&resize=pct:50&imageUrl=https://upload.wikimedia.org/wikipedia/commons/7/71/Brugge_Panorama.jpg

should return a slightly rotated, resized image


https://yourdomain.com/pyimgapi/deepzoom?

will create an image pyramid consisting of small tiles that can be used to zoom into image details with the [openseadragon](https://openseadragon.github.io/) viewer. The api aplies the requested image processing steps before creating the tiles pyramid. It returns a json like this:

    {"Format": "jpeg", "Overlap": "1", "TileSize": "254", "Size": {"Height": "312", "Width": "1261"}, "Url": "https://yourdomain.com/pyimgapi/tilesCache/https_upload_wikimedia_org_wikipedia_commons_7_71_Brugge_Panorama_jpg_files/"}

The json response can be used in the openseadragon viewer. See https://github.com/hbz/DeepZoomService#usage for an example.


https://yourdomain.com/pyimgapi/image/{id}/{region}/{size}/{rotation}/{targetfilename}

provides access to a minimalistic [**iiif**](https://iiif.io/) image api. The path components in the url must be given according to the iiif standard. The **\{id\}** component is the image name or id on the server that is given in **config.ini** under **url_pattern**:


    [image_server]
    url_pattern = https://example.org/path_to_images/{id}


The pyimgapi will fetch the image with the given id from that server and do the image processing defined in the other path components. See https://iiif.io/api/image/3.0/#4-image-requests for explanation of the path components


