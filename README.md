# pyimgapi
webservice for image processing with pyvips and libvips. It should implement at least the 
proccessing features needed for IIIF API. An image server may translate the IIIF Image API calls 
into parameters for this service and let the service do the job

## Documentation


### Installation for development:
Install virtual python environment:

    virtualenv --no-site-packages --distribute -p /usr/bin/python3.X pyimgapi
    cd pyimgapi/
    source ./bin/activate


### Install pyimgapi scripts in virtual environment
Download scripts and change into scripts directory:

    git clone https://github.com/bjquast/pyimgapi.git
    cd pyimgapi/
    python setup.py develop


### Configure Apache webserver

The pyimgapi has no authentication or authorization mechanism yet, but the basic authentication by the web server can be used. It is then strongly recommended to allow access only via https.

Setup a proxy for the wsgi-server in ssl configuration:

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
    
        # proxy for pyimgapi
        ProxyPass /pyimgapi http://localhost:6547/pyimgapi connectiontimeout=5 timeout=300
        ProxyPassReverse /pyimgapi http://localhost:6547/pyimgapi
        ProxyPreserveHost On
        ProxyRequests Off
    [...]
    
    </virtualhost>

The port (here 6547) can be changed in the development.ini and production.ini files.


Set a basic authentication user and password with:

    sudo htpasswd -c /etc/apache2/pyimgapi_passwd username



## Usage

development.ini can be used to allow the pyramid debug toolbar and the reload of templating system after changes. Thsi should not be activated in production systems, therefore, there is also an production.ini.

For development start the server with:

    pserve development.ini --reload
    
The service will then be available under: https://localhost/pyimgapi/


For production start the service with:

    pserve production.ini







