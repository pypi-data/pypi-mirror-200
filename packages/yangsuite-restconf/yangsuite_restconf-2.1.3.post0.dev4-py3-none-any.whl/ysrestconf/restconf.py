# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Python backend logic for restconf.

Nothing in this file should use any Django APIs.
"""
import json
import re
from collections import OrderedDict
from jinja2 import Template

from ysyangtree import YSContext, YSYangModels
from ysfilemanager import YSYangSet, split_user_set
from yangsuite.logs import get_logger
from ysrestconf.rmodels import ParseRestconf


log = get_logger(__name__)

# Max depth to generate from any selected tree node
MAX_DEPTH = 6

# Valid REST methods that this plugin supports
REST_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

ANSIBLE_TEMPLATE = """# Ansible will need some basic information to make sure
# it can connect to the target device before attempting
# sending a request using RESTCONF. Ansible will look
# in the same directory as the playbook file for ansible.cfg.
#
# Nearly all parameters in ansible.cfg can be overridden
# with ansible-playbook command line flags.

# Example of basic ansible.cfg file:
#
#[defaults]
#inventory = ./ansible_host
#

# Example of basic ansible_host file referred to in
# ansible.cfg inventory:
#
#[HOST_NAME_HERE]
#IP_ADDRESS_HERE
#
#[HOST_NAME_HERE:vars]
# ansible_connection: httpapi
# ansible_network_os: restconf
# ansible_httpapi_use_ssl: true
# ansible_httpapi_validate_certs: false
# ansible_httpapi_port: 443
# ansible_httpapi_restconf_root: /restconf/data/
# ansible_user: USERNAME_HERE
# ansible_password: PASSWORD_HERE
#

- name: {{ msg_name }}
  hosts: HOST_NAME_HERE
  gather_facts: no
  tasks:
    - name: {{ task_name }}
    {%- if method == 'get' %}
      ansible.netcommon.restconf_get:
        # Output can either be json or xml
        output: json
    {%- else %}
      ansible.netcommon.restconf_config:
        method: {{ method }}
        format: json
    {%- endif %}
        path: {{ path }}
        {% if body -%}
        content: |
          {{ body }}
        {%- endif -%}"""

OPENAPI_PATH_PARAMS_RE = re.compile(r'=\{.*\}')
CURLY_BRACES_CONTENT_RE = re.compile(r'{(.*?)}')


class ParseRestconfError(Exception):
    """General restconf parsing error."""

    def __init__(self, msg=''):
        if not msg:
            raise self
        self.message = msg


def nodes_match(swagobj, node_ids):
    """Check if filtering matches request."""
    if node_ids and not swagobj.tags or swagobj.tags and not node_ids:
        # The cached swagobj does not match the filtering request
        return False
    if swagobj.tags and node_ids:
        for node in swagobj.tags:
            if node not in node_ids:
                # The cached swagobj has different filters so get a new one
                return False
    return True


def get_restconf_parser(ysmodels, **req):
    """Get cached instance of swagger object."""
    node_ids = []

    nodes = req.get('nodes', None)
    names = req.get('models', None)
    user = req.get('user')
    yangset = req.get('yangset')
    host = req.get('host')
    proxyhost = req.get('proxyhost')
    ncparse = None

    try:
        ncparse = ysmodels.yangs[names[0]]
    except KeyError:
        """ If the module is not inside the YSYangModels object,
        create new YSYangModels object with it, and new YSContext
        """
        owner, setname = split_user_set(yangset)
        ys = YSYangSet.load(owner, setname)
        YSContext.discard_instance(setname, owner)
        ctx = YSContext(ys, setname, [], owner)
        ctx.load_module_files(names)
        ysmodels = YSYangModels(ctx, names)
        YSYangModels.store_instance(ysmodels, user)
        ncparse = ysmodels.yangs[names[0]]

    depth_limit = req.get('depthlimit', None)
    if nodes:
        node_ids = [node['schema_node_id'] for node in nodes]
    if not hasattr(ncparse, 'swagobj') or \
       ysmodels.modelnames != sorted(names) or \
       not nodes_match(ncparse.swagobj, node_ids) or \
       ncparse.host != host or \
       ncparse.depth_limit != depth_limit:
        # Not a match - need a new one
        try:
            """ Get YSContext from YSYangModels object,
            if the context does not have the correct modules loaded,
            load new modules
            """
            ctx = ysmodels.ctx
            ctx_has_correct_modules = False
            ctx_modules = ctx.modules
            for module in ctx_modules:
                if module[0] == names[0]:
                    ctx_has_correct_modules = True
                    break
            if not ctx_has_correct_modules:
                ctx.load_module_files(names)
        except RuntimeError:
            raise ParseRestconfError("Context: No such user")
        except ValueError:
            raise ParseRestconfError("Invalid yangset: " + str(yangset))
        except KeyError:
            raise ParseRestconfError("Context: Bad cache reference")
        except OSError:
            raise ParseRestconfError("No such yangset")
        if ctx is None:
            raise ParseRestconfError("User context not found")
        ncparse.swagobj = ParseRestconf(user, names[0], ctx, node_ids,
                                        host, depth_limit, proxyhost=proxyhost)
        ncparse.depth_limit = depth_limit
        ncparse.host = host
        ysmodels.yangs[names[0]] = ncparse
        YSYangModels.store_instance(ysmodels, user)

    if not hasattr(ncparse, 'swagobj'):
        raise ParseRestconfError('Unable to generate APIs')
    else:
        return ncparse.swagobj.get_header(user, page=0)


def generate_swagger(request):
    """Main accessor function for module."""
    user = request.get('user')

    # Do we have a cached yangset instance?
    ysmodels = YSYangModels.get_instance(user)

    if not ysmodels:
        yangset = request.get('yangset')
        models = request.get('models')
        ctx = YSContext.get_instance(user, yangset)

        ysmodels = YSYangModels(ctx, models)
        YSYangModels.store_instance(ysmodels, user)
    return get_restconf_parser(ysmodels, **request)


def get_parse_status(user):
    """Return status of current RESTCONF parser."""
    return ParseRestconf.get_status(user)


def get_header(request):
    """Return OpenAPI header with paths chunk coresponding to chosen page."""
    user = request.user.username
    page = int(request.GET.get('page'))
    return ParseRestconf.get_header(user, page)


class AnsiblePlaybook():
    def __init__(
        self, filename, task_name, msg_name, xpath, xpath_value,
        method, openapi_doc,
    ):
        self.filename = f'{filename}.yaml'
        self.task_name = task_name
        self.msg_name = msg_name
        self.xpath = xpath
        self.xpath_value = xpath_value
        self.method = method.lower()

        self.openapi_doc = openapi_doc

    @staticmethod
    def remove_path_params(path):
        if '/' not in path and '=' not in path:
            return path

        tokens = path.split('/')
        # Preserve token before equal sign for all path tokens
        formatted_path = '/'.join([
            token.split('=')[0]
            if '=' in token else token
            for token in tokens
        ])
        # Trim empty spaces
        formatted_path = formatted_path.replace(' ', '')
        # Trim invalid chars
        formatted_path = formatted_path.replace('{', '')
        formatted_path = formatted_path.replace('}', '')

        return formatted_path

    def get_path_and_body(self, openapi_doc, xpath, method):
        """Get RESTCONF resource path and body from OpenAPI 3.0 document"""
        paths_dict = {}
        # Most matched path in list of matched paths
        matched_path = None
        path = None
        body = None

        try:
            paths_dict = openapi_doc['paths']
        except KeyError:
            raise KeyError(
                'URL or paths keys are nonexistent in OpenAPI document.'
            )

        if not paths_dict:
            raise ValueError('Unable to retrieve paths')

        # Match XPath to path
        for path in paths_dict:
            # Remove keys and namespaces from path for comparison
            formatted_path = path
            formatted_path = self.remove_path_namespaces(formatted_path)
            formatted_path = self.remove_path_params(formatted_path)

            xpath_tokens = [token.strip() for token in xpath.split('/')[1:]]
            formatted_tokens = [
                token.strip() for token in formatted_path.split('/')
            ]
            # Check for equality after splitting xpath and formatted path
            if xpath_tokens == formatted_tokens[
                len(formatted_tokens) - len(xpath_tokens):
            ]:
                matched_path = path

        if not matched_path:
            raise ValueError(
                'XPath does not exist as a path in OpenAPI document'
            )

        # Get path object from document using matched path, and gen. url & body
        path_dict = paths_dict.get(matched_path, None).get(method, None)
        if path_dict:
            # Path is the matched path without the first slash token (data)
            path = '/'.join(matched_path.split('/')[2:])
            # Convert path's OpenAPI-syntax schema to dict if it exists
            if path_dict.get('requestBody', None):
                # Request has a body, method is one of: PATCH, PUT, POST
                path_content = path_dict['requestBody']['content']
                path_json_obj = path_content['application/yang-data+json']
                schema_obj = path_json_obj['schema']
                # Browse for request body schema obj in document
                schema = {}
                if schema_obj.get('$ref', None):
                    schema_ref = schema_obj['$ref']
                    schema_name = schema_ref.split('/')[-1]
                    schema = openapi_doc['components']['schemas'][schema_name]
                else:
                    schema = schema_obj
                # Parse schema to make body
                body = self.schema_to_json(schema, xpath)
        else:
            raise ValueError('This REST method is not supported')

        return (path, body)

    @staticmethod
    def params_exists(path):
        """Check for parameter existence in any given OpenAPI 3.0 path"""
        return re.search(OPENAPI_PATH_PARAMS_RE, path) is not None

    def schema_to_json(self, dictionary, xpath, data={}):
        """Transform OpenAPI 3.0 Schema object to JSON"""
        # Set of properties in dict that identify it will have children
        OPENAPI_PROPS = {'type', 'properties', 'items'}
        TYPES_TO_PROPS = {'object': 'properties', 'array': 'items'}
        child_type = 'object'
        tmp_dict = dictionary

        if isinstance(tmp_dict, OrderedDict):
            # Convert to dict from OrderedDict
            tmp_dict = json.loads(json.dumps(tmp_dict))

        if set(tmp_dict.keys()) & OPENAPI_PROPS:
            child_type = tmp_dict['type']
            tmp_dict = tmp_dict.get('properties', None)\
                or tmp_dict.get('items', None)
            if not tmp_dict:
                return data

        for key, value in tmp_dict.items():
            if isinstance(value, dict):
                value_keys = value.keys()
                if set(value_keys) & OPENAPI_PROPS and len(value_keys):
                    child_type = value['type']
                    value = value.get('properties', None)\
                        or value.get('items', None)
                    if not value and child_type not in TYPES_TO_PROPS.keys():
                        # Not nested anymore
                        data = {**data, key: self.xpath_value}
                    else:
                        if child_type == 'object':
                            data = {
                                **data,
                                key: self.schema_to_json(value, xpath, data)
                            }
                        elif child_type == 'array':
                            datum = self.schema_to_json(value, xpath, data)
                            data = {
                                **data,
                                key: [
                                    {datum_key: datum[datum_key]}
                                    for datum_key in datum.keys()
                                ]
                            }
        return data

    def get_params_map(self, path):
        """Return map of path element and its parameter name"""
        params_map = {}
        tokens = path.split('/')

        if not path or '/' not in path and '=' not in path:
            # No parameters in path
            return params_map

        for token in tokens:
            if '=' in token:
                param_tokens = token.split('=')
                param_ref = param_tokens[-1]
                param_ref = param_ref.replace('{', '')
                param_ref = param_ref.replace('}', '')
                params_map[param_tokens[0]] = param_ref

        return params_map

    @staticmethod
    def remove_path_namespaces(path):
        """Returns xpath with all namespaces removed"""
        if not path or '/' not in path or ':' not in path:
            return path

        tokens = path.split('/')
        return '/'.join([
            token.split(':')[-1] if ':' in token else token for token in tokens
        ])

    def gen_playbook_content(self):
        """Returns playbook content str and map of param names to OpenAPI ref.
        of that param name"""
        result = {}
        tplt = Template(ANSIBLE_TEMPLATE)
        path, body = self.get_path_and_body(
            self.openapi_doc, self.xpath, self.method
        )
        # Additional parameters that user needs to fill out in front-end
        params_map = self.get_params_map(path)

        result = tplt.render({
            'path': path,
            'method': self.method,
            'body': json.dumps(body) if body else None,
            'task_name': self.task_name,
            'msg_name': self.msg_name
        })

        return (result, params_map)
