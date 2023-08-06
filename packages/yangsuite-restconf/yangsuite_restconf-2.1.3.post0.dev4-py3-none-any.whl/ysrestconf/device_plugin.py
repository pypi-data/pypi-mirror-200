# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""RESTCONF device definitions."""
import traceback
import requests
from collections import OrderedDict
from yangsuite import get_logger
from ysdevices import YSDeviceProtocolPlugin
from ysdevices.utilities import encrypt_plaintext, decrypt_ciphertext

log = get_logger(__name__)


class RestconfPlugin(YSDeviceProtocolPlugin):
    """RESTCONF protocol extensions of YSDeviceProfile."""

    label = "RESTCONF"
    key = "restconf"

    @classmethod
    def data_format(cls):
        """Format of device settings fields."""
        result = OrderedDict()
        result['enabled'] = {
            'label': "Device supports RESTCONF",
            'type': 'boolean',
            'default': False,
        }
        result['encoding'] = {
            'label': "HTTP or HTTP(secure) encoding",
            'type': 'string',
            'default': 'https',
        }
        result['base_url'] = {
            'label': "RESTCONF base URL",
            'type': 'string',
            'default': '/restconf',
        }
        result['port'] = {
            'label': 'RESTCONF port',
            'type': 'int',
            'description': 'Port number RESTCONF listens on',
            'min': 1,
            'max': 65535,
            'default': 443,
            'required': True,
        }
        result['address'] = {
            'type': 'string',
            'description': 'Address or hostname to access via RESTCONF',
        }
        result['username'] = {
            'type': 'string',
            'description': 'Username to access the device via RESTCONF',
            'minLength': 1,
            'maxLength': 50,
        }
        result['password'] = {
            'type': 'password',
            'description': 'Password to access the device via RESTCONF',
            'minLength': 1,
            'maxLength': 50,
        }
        return result

    address = YSDeviceProtocolPlugin.inheritable_property(
        'address',
        docstring="Address for RESTCONF access if different from base address")
    username = YSDeviceProtocolPlugin.inheritable_property(
        'username',
        docstring="RESTCONF login username, if different from base username")
    password = YSDeviceProtocolPlugin.inheritable_property(
        'password',
        docstring="RESTCONF login password, if different from base password")

    def update(self, data):
        """Update dict function overwrite.

        Args:
          data (dict): Contains device settings.
        """
        if 'password' not in data or not data['password']:
            if 'encrypted_password' in data and data['encrypted_password']:
                data['password'] = decrypt_ciphertext(
                    data['encrypted_password'],
                    (data.get('username') or self.username))
        return super(RestconfPlugin, self).update(data)

    def dict(self):
        """Return content of this class."""
        data = super(RestconfPlugin, self).dict()
        data['encrypted_password'] = encrypt_plaintext(self._password,
                                                       self.username)
        del data['password']
        return data

    @classmethod
    def check_reachability(cls, devprofile):
        """Check to see if device can respond to RESTCONF connection."""
        try:
            sess = requests.Session()
            sess.auth = requests.auth.HTTPBasicAuth(
                devprofile.restconf.username,
                devprofile.restconf.password)
            sess.headers.update(
                {'Accept': 'application/yang-data+json, \
                            application/yang-data.errors+json',
                 'Content-type': 'application/yang-data+json'})
            host = devprofile.restconf.encoding + '://' + \
                devprofile.restconf.address + ':' + \
                str(devprofile.restconf.port) + devprofile.restconf.base_url
            result = sess.get(host, verify=False)
            result.raise_for_status()
            result = ('RESTCONF', True, '')

            return result
        except Exception as e:
            log.debug("RESTCONF check failed: %s", e)
            log.debug(traceback.format_exc())
            return ('RESTCONF', False, str(e))
