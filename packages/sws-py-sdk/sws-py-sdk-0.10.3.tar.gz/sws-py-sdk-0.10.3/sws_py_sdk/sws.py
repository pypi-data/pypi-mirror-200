""" This class is a representation of the Serato Web Services.
    The purpose is to improve the integration of Python with our APIs.
    Encapsulates the functionality required to communicate with the endpoints we provide.
    The definitions of each service will be contained in separate classes
"""
import base64

from sws_py_sdk import identity, license, ecom, cloudlib

service_uri_default = {
    'id': 'id.serato.com',
    'license': 'license.serato.com',
    'ecom': 'ecom.serato.com',
    'cloudlib': 'cloudlib.serato.com',
    # profile: 'profile.serato.com'
}


class Sws(object):

    def __init__(
        self,
        app_id,
        secret=None,
        user_id=0,
        timeout=3000,
        service_uri={},
        invalid_access_token_handler=None,
        test_env=False,
        cdn_auth_id=None,
        cdn_auth_secret=None,
    ):
        """
        Create SWS object
        config : object
            Configuration options
        appId : str
            Application ID
        secret : str
            Application secret
        user_id : int
            End user ID
        timeout : float
            Request timeout
        service_uri : object
            Base URIs for SWS services
        service_uri.id : str
            Base URI for SWS ID Service
        service_uri.license : str
            Base URI for SWS License Service
        auto_refresh : boolean
            Determines if the client will attempt to refresh the access token if invalid or expired.
        cdn_auth_id : str
            Client ID used to authenticate with test stack CDNs
        cdn_auth_secret : str
            Secret used to authenticate with test stack CDNs
        """
        self.app_id = app_id
        self.secret = secret
        self.user_id = user_id
        self.timeout = timeout
        self.access_token = ''
        self.refresh_token = ''
        self.service_uris = {
            'id': service_uri['id'] if 'id' in service_uri.keys() else service_uri_default['id'],
            'license': service_uri['license'] if 'license' in service_uri.keys() else service_uri_default['license'],
            'ecom': service_uri['ecom'] if 'ecom' in service_uri.keys() else service_uri_default['ecom'],
            'cloudlib': service_uri['cloudlib'] if 'cloudlib' in service_uri.keys() else service_uri_default['cloudlib']
        }

        self.service = {
            'id': identity.Identity(sws=self),
            'license': license.License(sws=self),
            'ecom': ecom.Ecom(sws=self),
            'cloudlib': cloudlib.Cloudlib(sws=self)
            # Define more clients here
        }
        self.invalid_access_token_handler = invalid_access_token_handler
        self.test_env = test_env
        self.cdn_auth_id = cdn_auth_id
        self.cdn_auth_secret = cdn_auth_secret

    def identity(self):
        """ Getter for the id service instance """
        return self.service['id']

    def license(self):
        """ Getter for the license service instance """
        return self.service['license']

    def ecom(self):
        """ Getter for the ecom service instance """
        return self.service['ecom']

    def cloudlib(self):
        """ Getter for the cloud library service instance """
        return self.service['cloudlib']

    def get_cdn_auth_header(self):
        """ Returns the x-serato-cdn-auth header, encoding the credentials used to access test stack CDNs
        """
        credentials = f'{self.cdn_auth_id}:{self.cdn_auth_secret}'
        encoded_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')
        return {'x-serato-cdn-auth': encoded_credentials}
