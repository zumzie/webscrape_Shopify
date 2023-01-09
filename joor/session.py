import time
import hmac
import json
from hashlib import sha256

try:
    import simplejson as json
except ImportError:
    import json

import re
from contextlib import contextmanager
from six.moves import urllib
from joor.api_access import ApiAccess
from joor.api_version import ApiVersion, Release, Unstable
import six

class ValidateException(Exception):
    pass

class Session(object):
    api_key = None
    secret = None
    protocol = "https"
    myshopify_domain = "myshopify.com"
    port = None
    
    @classmethod
    def setup(cls, **kwargs):
        for k, v in six.iteritems(kwargs):
            setattr(cls, k, v)

    @classmethod
    @contextmanager
    def temp(cls, domain, version, token):
        import joor

        original_domain = joor.JoorResource.url
        original_token = joor.JoorResource.get_headers().get("X-Joor-Access-Token")
        original_version = joor.JoorResource.get_version() or version
        original_session = joor.Session(original_domain, original_version, original_token)

        session = Session(domain, version, token)
        joor.JoorResource.activate_session(session)
        yield
        joor.JoorResource.activate_session(original_session)

    def __init__(self, store_url, version=None, token=None, access_scopes=None)