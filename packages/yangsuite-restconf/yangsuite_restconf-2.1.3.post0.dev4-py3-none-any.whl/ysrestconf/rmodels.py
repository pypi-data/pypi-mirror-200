# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
"""Prepare YANG Suite JSON file for swagger interface."""
import pyang
import itertools
import math
from collections import OrderedDict
from ysyangtree.ymodels import (
    ParseYang,
    NON_SCHEMA_NODETYPES,
    NON_DATA_NODETYPES
)


class ParseRestconfError(Exception):
    """General restconf parsing error."""

    def __init__(self, msg=''):
        """Set message."""
        if not msg:
            raise self
        self.message = msg


class ParseRestconf(ParseYang):
    """Prepare YANG Suite JSON file for swagger interface."""

    parse_status = {}
    cached_head = {}
    cached_paths = {}
    paths_per_page = 50

    @classmethod
    def get_status(cls, reference):
        """Return status of RESTCONF parsing relating to reference.

        Args:
          reference (str): Index to ParseRestconf instance.
        Returns:
          (str)
        """
        rcparse = cls.parse_status.get(reference, None)
        if rcparse:
            return rcparse.status
        return ''

    @classmethod
    def get_header(cls, user: str, page: int) -> dict:
        """Get header with paths chunk.

        Args:
          user (str): Key to cached header and paths data.
          page (int): Page index.
        Returns:
          (dict)
        """
        head = dict(
            paths=dict(
                itertools.islice(
                    cls.cached_paths[user].items(),
                    page * cls.paths_per_page,
                    (page + 1) * cls.paths_per_page)))

        page_count = cls.cached_head[user]['pageCount']
        pagination = {
            'pagination': {
                'pageIndex': page,
                'next': False if page == (page_count - 1) else True,
                'previous': False if page == 0 else True,
            }
        }
        head.update(pagination)
        head.update(cls.cached_head[user])
        return head

    def __init__(self, user, name, ctx, tags, host, depth_limit,
                 swagger_version='3.0.3', proxyhost='localhost:8480'):
        """Parse YANG models."""
        self.status = 'Initializing'
        self.schema_refs = OrderedDict()
        self.swagger_version = swagger_version
        self.spec = None
        self.pathkeys = []
        self.keynames = {}
        self.included_xpath = ''
        self.host = host
        self.proxyhost = proxyhost
        self.depth_limit = depth_limit
        super().__init__(name, '', ctx)
        self.tags = tags
        self.parse_status[user] = self
        self.generate_rc_tree()
        self.cached_head[user] = self.gen_header()
        self.cached_paths[user] = self.spec['paths']
        if user in self.parse_status:
            # Done parsing so remove instance
            self.parse_status.pop(user)
        self._tagnames = []

    @property
    def tags(self):
        """Tags refer to xpath or whole module in generated API."""
        return self._tags

    @tags.setter
    def tags(self, tags):
        if tags:
            self._record_all = False
            self._filter = True
            self._tags = tags
            self._tagnames = []
            # add tagnames for easier comparison
            for tag in tags:
                tagname = tag.split('/')[-1]
                """ filter out the first part of the colon in tag name,
                ex. ios-qos in ios-qos:map-list """
                if ':' in tagname:
                    tagname = tag.split(':')[-1]
                self._tagnames.append(tagname)
        else:
            self._record_all = True
            self._filter = False
            self._tags = ['/' + self.name]

    @property
    def host(self):
        """Device profile object."""
        return self._host

    @host.setter
    def host(self, host):
        if not host.base.address:
            raise ParseRestconfError('No IP address')
        dev = host.base.address
        if host.restconf.address:
            dev = host.restconf.address
        dev += ':' + str(host.restconf.port)
        self._base_url = host.restconf.base_url
        self._encoding = host.restconf.encoding
        self._host = dev
        self.user = host.restconf.username
        self.pwd = host.restconf.password

    def filter_statements(self, stmt, parent_data):
        """Move to next statement."""
        xp = self.get_stmt_node_id(stmt,
                                   mode='schema')

        if not self._filter:
            self.status = 'No filtering'
            return True

        for node in self.tags:
            if xp == node:
                self.status = 'End of filtering'
                return True
            elif stmt.keyword == 'list':
                if node.startswith(xp):
                    # need the keys so we have to start here
                    self.status = 'Keys detected upstream of filtering'
                    return True

        self.status = 'Filtering ' + xp
        return False

    def generate_spec(self, child, spec):
        """Generate RESTCONF specification."""
        if self.filter_statements(child, spec):
            spec.update(self.get_node_data(child, spec))
        else:
            if not hasattr(child, 'i_this_not_supported'):
                if hasattr(child, "i_children"):
                    for ch in child.i_children:
                        self.generate_spec(ch, spec)

    def generate_tree(self, node_callback=None):
        """Skip the parent class call to generate_tree."""
        pass

    def generate_rc_tree(self):
        """The swagger generator."""
        self.status = 'Retrieving module data'
        self.module_data = self.get_module_node_data()

        spec = OrderedDict({'paths': {}})

        for child in self.module.i_children:
            if child.keyword in self.included_nodetypes:
                self.generate_spec(child, spec)

        self.spec = spec

    def gen_header(self):
        """Setup swagger header for this module."""
        head = OrderedDict()
        head['openapi'] = self.swagger_version
        head['info'] = {
            'description': 'HOST DESTINATION:  {0}://{1} ({2})'.format(
                self._encoding,
                self.host,
                'proxy through YANG Suite server'),
            'title': 'OpenAPI v{0}'.format(self.swagger_version),
            'version': self.swagger_version,
        }
        head['servers'] = {
            'url': '/restconf/proxy/{0}://{1}{2}'.format(
                self._encoding,
                self.host,
                self._base_url
            )
        }
        head['components'] = {
            'securitySchemes': {
                'basicAuth': {
                    'type': 'http',
                    'scheme': 'basic',
                },
                'bearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'description': 'Enter the token with the `X-auth: ` prefix, e.g. \"`X-auth`:`abcde12345`.'  # noqa
                },
            }
        }
        head['security'] = [{
            'basicAuth': [],
            'bearerAuth': [],
        }]
        head['servers'] = [
            {
                'url': '/restconf/proxy/{}://{}{}'.format(
                    self._encoding,
                    self.host,
                    self._base_url
                ),
                'description': 'YANG SUITE Proxy RESTCONF API'
            }
        ]
        head['components'].update(OrderedDict({
            'schemas': self.schema_refs
        }))
        head['pageCount'] = math.ceil(
            len(self.spec['paths']) / self.paths_per_page)
        return head

    def gen_property(self, node):
        """Generate a simple Schema object."""
        dtype = OrderedDict()
        data = node['data']
        if 'datatype' not in data:
            # TODO: contaner or list so what works in schema?
            return {}

        if 'int' in data['datatype']:
            dtype['type'] = 'integer'
            dtype['format'] = data['datatype']
        elif data['datatype'] == 'decimal64':
            dtype['type'] = 'number'
            dtype['format'] = 'double'
        elif data['datatype'] == 'boolean':
            dtype['type'] = data['datatype']
        elif data['datatype'] == 'enumeration':
            dtype['type'] = 'string'
            enums = []
            for name, val in data['typespec']['values']:
                enums.append(name)
            dtype['enum'] = enums
        elif data['datatype'] == 'leafref':
            # TODO: not sure what to do here
            dtype['type'] = 'string'
            dtype['x-path'] = ''
        elif data['datatype'] == 'identityref':
            dtype['type'] = 'string'
            refs = []
            if hasattr(data, 'typespec') or data.get('typespec'):
                for ref in data['typespec']['iref']:
                    # replace prefixes with full model name
                    modelref = ref['namespace'].split(':')[-1]
                    refname = ref['name'].split(':')[1]
                    refs.append(modelref + ':' + refname)
                dtype['enum'] = refs
            elif hasattr(data, 'options') or data.get('options'):
                for ref in data['options']:
                    # replace prefixes with full model name
                    refs.append(ref)
                dtype['enum'] = refs
        elif data['datatype'] == 'empty':
            # TODO: not sure about this one
            dtype['type'] = 'string'

        # map all other types to string
        else:
            dtype['type'] = 'string'

        return dtype

    def gen_list_body(self, stmt, parent_data, data, current_depth):
        """Generate one API per list and always use schema."""
        body = OrderedDict()

        children_names = [ch.arg for ch in stmt.i_children]
        if not children_names:
            return body

        # create a reference to list
        if hasattr(stmt, 'parent'):
            # prefix with parent to prevent name conflicts
            schema_name = stmt.parent.arg.title() + \
                stmt.arg.title() + 'SchemaById'
        else:
            # TODO: is list ok at top?  no container?  would this work?
            schema_name = stmt.arg.title() + 'TopSchemaById'

        schema_name_xml = schema_name + 'Xml'
        if schema_name not in self.schema_refs:
            properties = self.gen_item_props(stmt, current_depth)
            sanitized_properties = OrderedDict({})
            for key in properties.keys():
                if key in children_names:
                    sanitized_properties[key] = properties[key]
            # TODO: better be a key!
            schema = OrderedDict({
                'type': 'object',
                'properties': OrderedDict({
                    stmt.arg: OrderedDict({
                        'type': 'array',
                        'items': OrderedDict({
                            'type': 'object',
                            'properties': sanitized_properties
                        })
                    }),
                }),
            })
            schema_xml = OrderedDict({
                **schema,
                'xml': {
                    'name': stmt.arg,
                },
            })

            self.schema_refs[schema_name] = schema
            self.schema_refs[schema_name_xml] = schema_xml

            body = OrderedDict({
                'description': self.get_subst_arg(stmt, 'description'),
                'required': True,
                'content': OrderedDict({
                    'application/yang-data+json': OrderedDict({
                        'schema': {
                            '$ref': '#/components/schemas/{0}'.format(
                                schema_name
                            )
                        },
                    }),
                    'application/yang-data+xml': OrderedDict({
                        'schema': {
                            '$ref': '#/components/schemas/{0}'.format(
                                schema_name_xml
                            )
                        },
                    }),
                })
            })

        return body

    def gen_container_list_body(self, stmt, current_depth):
        """Generate container API with schema if needed."""
        body = OrderedDict()
        if not hasattr(stmt, 'i_children'):
            return body

        children_names = [ch.arg for ch in stmt.i_children]

        if not children_names:
            return body

        if hasattr(stmt, 'parent'):
            # prefix with parent to prevent name conflicts
            schema_name = stmt.parent.arg.title() + \
                stmt.arg.title() + 'SchemaById'
        else:
            schema_name = stmt.arg.title() + 'SchemaById'

        schema_name_xml = schema_name + 'Xml'

        if schema_name not in self.schema_refs:
            required = []
            properties = self.gen_item_props(stmt, current_depth)
            if required:
                properties['required'] = required
            sanitized_properties = OrderedDict({})
            for key in properties.keys():
                if key in children_names:
                    sanitized_properties[key] = properties[key]

            schema = OrderedDict({
                'type': 'object',
                'properties': OrderedDict({
                    stmt.arg: OrderedDict({
                        'type': 'object',
                        'properties': OrderedDict(sanitized_properties),
                    }),
                }),
            })
            self.schema_refs[schema_name] = schema
            self.schema_refs[schema_name_xml] = OrderedDict({
                **schema,
                'xml': {
                    'name': stmt.arg,
                },
            })

            body = OrderedDict({
                'description': self.get_subst_arg(stmt, 'description'),
                'required': True,
                'content': OrderedDict({
                    'application/yang-data+json': OrderedDict({
                        'schema': {
                            '$ref': '#/components/schemas/{0}'.format(
                                schema_name
                            )
                        },
                    }),
                    'application/yang-data+xml': OrderedDict({
                        'schema': {
                            '$ref': '#/components/schemas/{0}'.format(
                                schema_name_xml
                            )
                        },
                    })
                })
            })

        return body

    def merge_dictionaries(self, a, b, path=None):
        "Merge dictionary b into dictionary a"
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge_dictionaries(a[key], b[key], path + [str(key)])
                elif a[key] == b[key] or isinstance(a[key], type(b[key])):
                    # same leaf value
                    pass
                else:
                    raise Exception('Conflict at %s' % '.'.join(
                        path + [str(key)]
                    ))
            else:
                a[key] = b[key]
        return a

    def add_keys_generate_pathname(self, node, xpath, stmtkeys=[]):
        """ Add keys to self's pathkeys and return pathname"""
        def generate_keys(node, stmtkeys, keys=[]):
            """ Process given node and its children to get keys props """
            def gen_leaf_prop(node):
                dtype = {'data': {}}
                self.get_stmt_specific_data(node, dtype)
                prop = self.gen_property(dtype)

                return prop

            if node:
                if hasattr(node, 'i_children'):
                    # if the node has children, generate keys for all key nodes
                    for child in node.i_children:
                        if child.arg in stmtkeys:
                            # some methods will need this as a path parameter
                            prop = gen_leaf_prop(child)
                            keys.append(OrderedDict({
                                'name': child.arg,
                                'in': 'path',
                                'required': False,
                                'schema': prop,
                            }))
                elif node.arg in node.parent.search_one('key').split(' '):
                    # if the node is a key itself, then generate key prop
                    prop = gen_leaf_prop(node)
                    # some methods will need this as a path parameter
                    keys.append(OrderedDict({
                        'name': node.arg,
                        'in': 'path',
                        'required': False,
                        'schema': prop,
                    }))

            return keys

        # Add parameters to xpath
        keys = generate_keys(node, stmtkeys)
        owner = xpath[xpath.rfind('/') + 1:]
        pathname_concat = ''
        if len(keys):
            for i in range(len(keys)):
                paramname = '{0}-{1}'.format(
                    owner, keys[i].get('name')
                )
                pathname = ''
                if i == 0:
                    pathname = '={' + paramname + '}'
                else:
                    pathname += ',' \
                        + keys[i].get('name') \
                        + '={' + paramname \
                        + '}'
                pathname_concat += pathname
                keys[i]['pathname'] = pathname
                keys[i]['paramname'] = paramname

        if len(keys) > 1:
            self.pathkeys.append((xpath, pathname_concat, keys))
            return pathname_concat
        self.pathkeys.append((xpath, pathname, keys))
        return pathname

    def gen_item_props(self, node, current_depth, depth=0, item_props={}):
        """ Generate properties to be inserted into a container's/list's
        body using breadth-first traversal, and traverse from child to root
        when any leaf is reached to transform tree data structure into valid
        OpenAPI 3.0 document structure"""
        def gen_leaf_or_choice_item_props(self, node, depth):
            """ Generate props for node once leaf or choice is reached """
            def gen_prop(node, prop={}):
                """Generate prop for single leaf/leafref/choice/leaf-list"""
                node_type = None

                if node.keyword == 'type':
                    node_type = node.arg
                else:
                    node_type = node.keyword
                if node_type in ['leaf', 'leafref', 'leaf-list']:
                    dtype = {'data': {}}
                    self.get_stmt_specific_data(node, dtype)
                    prop = self.gen_property(dtype)
                elif node_type == 'choice':
                    for case in node.i_children:
                        for case_ch in case.i_children:
                            dtype = {'data': {}}
                            self.get_stmt_specific_data(case_ch, dtype)
                            prop[case_ch.arg] = self.gen_property(dtype)
                return prop

            prop = gen_prop(node)
            temp_props = {}
            prev_node = node
            current_node = node

            for i in range(depth):
                # currently at the lowest depth
                # go back up in depth and generate nested dict
                if i == 0:
                    if depth == 1:
                        temp_props[node.arg] = prop
                    else:
                        temp_props[node.parent.arg] = {'type': 'object'}
                        temp_props[node.parent.arg]['properties'] = {
                            node.arg: prop
                        }
                        current_node = node.parent
                else:
                    if current_node.arg not in temp_props.keys():
                        prop_no_properties = temp_props[prev_node.arg]
                        prop_with_properties = {
                            'properties': temp_props[prev_node.arg],
                            'type': 'object'
                        }
                        if 'properties' in temp_props[prev_node.arg]:
                            temp_props[current_node.arg] = {
                                'properties': {
                                    prev_node.arg: prop_no_properties
                                },
                                'type': 'object'
                            }
                        else:
                            temp_props[current_node.arg] = {
                                'properties': {
                                    prev_node.arg: prop_with_properties
                                },
                                'type': 'object'
                            }
                    prev_node = current_node
                    current_node = current_node.parent

            depth -= 1
            # merge the newly generated item props to the existing item props
            merged_item_props = self.merge_dictionaries(item_props, temp_props)
            return (merged_item_props, depth)

        # check if node exists before generating anything
        if node:
            """ if depth limit is reached, stop at current node and traverse
            back up to root node and generate body """
            if self.depth_limit and current_depth + depth > self.depth_limit:
                if node.keyword in ['container', 'list']:
                    temp_props = {}
                    last_key = ''

                    for i in range(depth):
                        if i == 0:
                            if depth == 1:
                                temp_props[node.arg] = {
                                    'properties': {}, 'type': 'object'
                                }
                            else:
                                temp_props[node.parent.arg] = {}
                                temp_props[node.parent.arg][node.arg] = {
                                    'properties': {},
                                    'type': 'object'
                                }
                                last_key = node.parent.arg
                        elif 'properties' not in temp_props[
                            node.parent.arg
                        ].keys():
                            temp_props[node.parent.arg] = {
                                'properties': temp_props[last_key],
                                'type': 'object'
                            }
                            last_key = node.parent.arg

                    depth -= 1
                    item_props = self.merge_dictionaries(
                        item_props, temp_props
                    )
                elif node.keyword in [
                        'leaf', 'leafref', 'choice', 'leaf-list']:
                    depth -= 1
                    item_props, depth = gen_leaf_or_choice_item_props(
                        self, node, depth
                    )
            else:
                """ if depth limit is not reached, go to next depth or generate
                item_props if leaf/choice is reached """
                if node.keyword in self.included_nodetypes:
                    if node.keyword in [
                            'leaf', 'leafref', 'choice', 'leaf-list']:
                        item_props, depth = gen_leaf_or_choice_item_props(
                            self, node, depth
                        )
                    else:
                        depth += 1
                        for ch in node.i_children:
                            item_props = self.gen_item_props(
                                ch,
                                current_depth,
                                depth=depth,
                                item_props=item_props
                            )

        return OrderedDict(item_props)

    def gen_input_body(self, stmt, parent_data, data, current_depth):
        """Generate rpc input API with schema if needed."""
        # add max recursion depth of 5
        body = {}
        if not hasattr(stmt, 'i_children'):
            return body

        children = [ch for ch in stmt.i_children]
        if not children:
            return body

        if hasattr(stmt, 'parent'):
            # prefix with parent to prevent name conflicts
            schema_name = stmt.parent.arg.title() + \
                stmt.arg.title() + 'SchemaById'
        else:
            schema_name = stmt.arg.title() + 'SchemaById'

        if schema_name not in self.schema_refs:
            item_props = self.gen_item_props(stmt, current_depth)
            required = []

            i_props = OrderedDict({'properties': item_props})
            if required:
                i_props['required'] = required

            items = OrderedDict({'type': 'array',
                                 'items': i_props})
            properties = OrderedDict({stmt.parent.arg: items})
            define = OrderedDict({
                'description': self.get_subst_arg(stmt, 'description'),
                'properties': properties})
            self.schema_refs[schema_name] = define
        body = OrderedDict({
            'description': self.get_subst_arg(stmt, 'description'),
            'required': True,
            'content': OrderedDict({
                'application/yang-data+json': OrderedDict({
                    'schema': OrderedDict({
                        'type': 'object',
                        'properties': properties,
                    })
                }),
                'application/yang-data+xml': OrderedDict({
                    'schema': OrderedDict({
                        'xml': {
                            'name': stmt.arg
                        },
                        'properties': properties,
                    })
                })
            })
        })

        return body

    def gen_leaf_body(self, node, method):
        """Generate one API per container and add body."""
        # GET method does not support having a request body
        if str(method).lower() == 'get':
            return None
        data = node['data']
        body = OrderedDict({
            'description': data['description'],
            'required': True,
            'content': OrderedDict({
                'application/yang-data+json': OrderedDict({
                    'schema': OrderedDict({
                        'type': 'object',
                        'required': [
                            data['name']
                        ],
                        'properties': {
                            data['name']: self.gen_property(node),
                        },
                    })
                }),
                'application/yang-data+xml': OrderedDict({
                    'schema': OrderedDict({
                        'xml': {
                            'name': data['name']
                        },
                        'type': 'object',
                        'required': [
                            data['name']
                        ],
                    })
                })
            })
        })

        # DELETE method does not require a body
        if str(method).lower() == 'delete':
            body['required'] = False

        return body

    responses = OrderedDict({
        '200': {
            'description': 'Successful OK',
            'content': {
                'application/yang-data+json': {},
                'application/yang-data+xml': {},
            }
        },
        '400': {
            'description': 'Internal error',
            'content': {
                'application/yang-data+json': {},
                'application/yang-data+xml': {},
            }
        },
        '405': {
            'description': 'Method not allowed',
            'content': {
                'application/yang-data+json': {},
                'application/yang-data+xml': {},
            }
        },
        '500': {
            'description': 'Internal server error',
            'content': {
                'application/yang-data+json': {},
                'application/yang-data+xml': {},
            }
        },
    })

    method = OrderedDict(
        {'description': '',
         "operationId": ''}
    )

    def gen_key_parameters(self, xpath, params=[]):
        """Gen key parameters if present in xpath"""
        for path, pathname, keys in self.pathkeys:
            if xpath.startswith(path):
                for key in keys:
                    if pathname in xpath:
                        param = key.copy()
                        param['name'] = key['paramname']
                        # remove pathname and paramname from param
                        param.pop('pathname', None)
                        param.pop('paramname', None)
                        if param not in params:
                            params.insert(0, param)
        if not params:
            return None
        return params

    def gen_method(self, method, name, xpath, body=None,
                   keyparams=None, operation_id=None):
        """Generate method."""
        head = OrderedDict()
        if operation_id is None:
            head['operationId'] = method.title() + name.title() + 'ById'
        else:
            head['operationId'] = operation_id
        # every method except GET and DELETE can have a req body
        if body and str(method).lower() not in ['get', 'delete']:
            head['requestBody'] = body
        if keyparams and len(keyparams):
            parameters = [
                param for param in keyparams if param['name'] in xpath
            ]
            head['parameters'] = parameters
        head['responses'] = self.responses
        return head

    def gen_list_create_methods(self, stmt, body, xpath, access):
        """Create methods for xpath of a list."""
        methods = OrderedDict()
        keyparams = self.gen_key_parameters(xpath)

        if access != 'read-only':
            for i in ['patch', 'put', 'post']:
                methods[i] = self.gen_method(
                    i, stmt.arg, xpath, body=body, keyparams=keyparams
                )

        methods['get'] = self.gen_method(
            'get', stmt.arg, xpath, body=None, keyparams=keyparams
        )

        return methods

    def gen_list_get_method(self, stmt, params, xpath):
        """Get method for xpath of a list."""
        methods = OrderedDict()
        keyparams = self.gen_key_parameters(xpath)
        methods['get'] = self.gen_method(
            'get', stmt.arg, xpath, keyparams=keyparams,
            operation_id=f"Get{stmt.arg.title()}ElemById"
        )

        return methods

    def gen_list_delete_method(self, stmt, params, xpath):
        """Delete method for xpath of a list."""
        methods = OrderedDict()

        keyparams = self.gen_key_parameters(xpath)
        methods['delete'] = self.gen_method(
            'delete', stmt.arg, xpath, keyparams=keyparams
        )

        return methods

    def gen_leaf_methods(self, stmt, data, path_items, xpath, access):
        """Create methods for xpath of a leaf."""
        methods_list = ['patch', 'put', 'get']
        no_body_methods_list = ['delete']
        methods = OrderedDict()

        # Xpath post processing for leaves that has a key leaf in the upper lvl
        if self.pathkeys:
            pathkey = self.pathkeys[-1]
            keys = pathkey[-1]
            target_key = keys[-1]
            paramname = target_key['paramname']
            pathname = target_key['pathname']
            parent_arg = paramname.replace(
                '-{0}'.format(target_key['name']), ''
            )
            node_arg = target_key['name']

            if parent_arg \
               and node_arg \
               and paramname not in xpath:
                xpath_elems = xpath.split('/')
                target_index = -2

                try:
                    target_index = xpath_elems.index(parent_arg)
                except ValueError:
                    pass

                if len(keys) > 1:
                    i = 0
                    for key in keys:
                        if i == 0:
                            xpath_elems[target_index] += key['pathname']
                        else:
                            xpath_elems[target_index] += ',{0}={1}'.format(
                                key['name'], key['pathname']
                            )
                        i += 1
                else:
                    xpath_elems[target_index] += pathname

                xpath = '/'.join(xpath_elems)

        keyparams = self.gen_key_parameters(xpath)

        if access in ['read-write', 'write']:
            for method in methods_list:
                body = self.gen_leaf_body(path_items, method)
                methods[method] = self.gen_method(
                    method, stmt.arg, xpath, body=body, keyparams=keyparams
                )
            for method in no_body_methods_list:
                methods[method] = self.gen_method(
                    method, stmt.arg, xpath, body=None, keyparams=keyparams
                )

            data[xpath] = methods
        else:
            methods['get'] = self.gen_method(
                'get', stmt.arg, xpath, body=None, keyparams=keyparams
            )

        data[xpath] = methods

    def gen_container_methods(self, stmt, data, body, xpath, access):
        """Create container methods."""
        methods = OrderedDict()
        keyparams = self.gen_key_parameters(xpath)

        if access in ['read-write', 'write']:
            for i in ['patch', 'put', 'post']:
                methods[i] = self.gen_method(
                    i, stmt.arg, xpath, body=body, keyparams=keyparams
                )
            # DELETE methods do not have request body
            methods['delete'] = self.gen_method(
                'delete', stmt.arg, xpath, body=None, keyparams=keyparams
            )

        # GET methods do not have request body
        methods['get'] = self.gen_method(
            'get', stmt.arg, xpath, body=None, keyparams=keyparams
        )

        data[xpath] = methods

    def gen_input_method(self, stmt, data, params, xpath, access):
        """Create rpc input methods."""
        methods = OrderedDict()

        methods['post'] = self.gen_method('post', stmt.arg, xpath, params)

        data[xpath.replace('data', 'operations', 1)] = methods

    def get_node_data(
        self, stmt, parent_data=OrderedDict({'paths': ''}), current_depth=0
    ):
        """Overwrite retrieval of node data to get only swagger parameters."""
        data = OrderedDict()
        path_items = OrderedDict()
        access = ''
        pfx = ''

        if stmt.keyword in ['output', 'notification']:
            return parent_data

        if stmt.i_module.i_prefix != self.pfx:
            pfx = stmt.i_module.i_prefix + ":"

        node = {'id': next(self.nodeid),
                'text': pfx + stmt.arg}

        icon = self.STMT_ICONS.get(stmt.keyword, 'glyphicon-alert')
        # Some types (e.g. container) may set no icon, preferring default
        if icon:
            node['icon'] = 'glyphicon ' + icon

        path_items['data'] = OrderedDict({'name': stmt.arg,
                                          'nodetype': stmt.keyword})

        if stmt.keyword in ['leaf', 'leaf-list']:
            path_items['data']['datatype'] = ''

        self.set_data_subst_arg(path_items['data'],
                                stmt,
                                'description',
                                default='')

        path_items['data']['description'] = self.get_subst_arg(stmt,
                                                               'description')

        # Work aroung pyang bug:
        # https://github.com/mbj4668/pyang/issues/383
        if pyang.statements.is_mandatory_node(stmt) or (
                stmt.keyword in ('choice', 'anyxml', 'anydata') and
                stmt.search_one('mandatory') and
                stmt.search_one('mandatory').arg == 'true'
        ):
            path_items['mandatory'] = 'true'
            path_items['icon'] = "glyphicon glyphicon-exclamation-sign"

        # Get any additional data based on the statement keyword
        self.get_stmt_specific_data(stmt, path_items)
        if 'icon' in path_items:
            path_items.pop('icon')

        #
        # Advanced data for skilled users and/or programmatic APIs
        #
        if stmt.keyword not in NON_SCHEMA_NODETYPES:
            if parent_data and 'operations' in parent_data and any(
                    op in ['input', 'output', 'notification']
                    for op in parent_data['operations']):
                # Input/output/notification subtrees all have the same
                # access and operations as their parents, as they're not
                # part of the data tree.
                access = parent_data['access']
            else:
                access = self.get_access(stmt)
                self.get_allowed_ops(stmt, path_items)

        xpath = self.get_stmt_node_id(stmt, mode='restconf')
        if xpath:
            self.status = 'Processing ' + xpath
            data[xpath] = OrderedDict()

        params = []

        keystmt = stmt.search_one('key')
        stmtkeys = []
        pathname = ''
        if keystmt:
            stmtkeys = keystmt.arg.split(" ")
            pathname = self.add_keys_generate_pathname(stmt, xpath, stmtkeys)

            if current_depth == 0 and stmt.arg not in self._tagnames:
                xpath += pathname

        if stmt.keyword == 'list':
            if (current_depth == 0 and stmt.arg in self._tagnames) \
              or current_depth > 0:
                body = self.gen_list_body(
                    stmt, parent_data, data, current_depth
                )
                data[xpath] = self.gen_list_create_methods(
                    stmt, body, xpath, access
                )
                # No path parameters for patch and put
                data[xpath + pathname] = self.gen_list_get_method(
                    stmt,
                    params,
                    xpath + pathname)
                if access != 'read-only':
                    data[xpath + pathname].update(
                        self.gen_list_delete_method(stmt, params, xpath))
            elif current_depth == 0 and stmt.arg not in self._tagnames:
                current_depth -= 1

        elif stmt.keyword in ['leaf', 'leafref']:
            if not hasattr(stmt, 'i_is_key'):
                if (current_depth == 0 and stmt.arg in self._tagnames) \
                  or current_depth > 0:
                    self.gen_leaf_methods(
                        stmt, data, path_items, xpath, access
                    )
                elif current_depth == 0 and stmt.arg not in self._tagnames:
                    current_depth -= 1

        elif stmt.keyword == 'container':
            if (current_depth == 0 and stmt.arg in self._tagnames) \
              or current_depth > 0:
                body = self.gen_container_list_body(stmt, current_depth)
                self.gen_container_methods(stmt, data, body, xpath, access)
            elif current_depth == 0 and stmt.arg not in self._tagnames:
                current_depth -= 1
        elif stmt.keyword == 'input':
            body = self.gen_input_body(stmt, parent_data, data, current_depth)
            self.gen_input_method(stmt, data, body, xpath, access)
            parent_data['paths'].update(data)
        if self._record_all and stmt.keyword not in NON_DATA_NODETYPES:
            # recording all APIs
            parent_data['paths'].update(data)
        else:
            schema_id = self.get_stmt_node_id(stmt, mode='schema')
            for tag in self.tags:
                if len(schema_id) < len(tag):
                    break
                if tag in schema_id:
                    # still recording APIs
                    if stmt.keyword not in NON_DATA_NODETYPES:
                        parent_data['paths'].update(data)
                    break
            else:
                return parent_data

        if not hasattr(stmt, 'i_this_not_supported'):
            if hasattr(stmt, "i_children"):
                if self.depth_limit and current_depth >= self.depth_limit:
                    return parent_data
                current_depth += 1
                for child in self.i_children_ordered(stmt, data):
                    if child.keyword in self.included_nodetypes:
                        self.get_node_data(
                            child, parent_data, current_depth=current_depth
                        )

        return parent_data

    def get_stmt_node_id(self, stmt, mode='schema'):
        """Build the schema or data node identifier (XPath) for a statement.

        Helper method to :meth:`get_node_data`.

        .. seealso:: :meth:`pyang.statements.mk_path_str`

        Args:
          stmt (pyang.statements.Statement) Statement to process.
          mode (str): One of 'schema' or 'data'.
          prefix_all (bool): If True, add namespace prefixes to all
            identifiers, even those in the current module and submodules.
            If False, only external module identifiers will be prefixed.

        Returns:
          str: XPath for schema or data node identifier, or None for nodes
            not in the schema tree
        """
        if mode not in ['data', 'schema', 'restconf']:
            raise ValueError

        path_nodes = []
        # Iterate upwards from this statement until reaching the top
        while stmt.keyword not in ['module', 'submodule']:
            if stmt.keyword in NON_SCHEMA_NODETYPES:
                return None
            elif mode == 'restconf' and stmt.keyword not in NON_DATA_NODETYPES:
                path_nodes.append((stmt.i_module.arg, stmt.arg))
            elif mode == 'schema' or stmt.keyword not in NON_DATA_NODETYPES:
                if stmt.i_module.i_prefix != self.pfx:
                    path_nodes.append(stmt.i_module.i_prefix + ":" + stmt.arg)
                else:
                    path_nodes.append(stmt.arg)

            stmt = stmt.parent

        path_nodes.reverse()

        if mode == 'restconf':
            saved_mods = []
            new_path = []
            for node in path_nodes:
                if node[0] not in saved_mods:
                    saved_mods.append(node[0])
                    new_path.append(node[0] + ':' + node[1])
                else:
                    new_path.append(node[1])

            new_path = '/data/' + '/'.join(new_path)

            if self.pathkeys:
                for xpath, pathname, keys in self.pathkeys:
                    if new_path.startswith(xpath):
                        for k in keys:
                            # this is a list so don't add key in path
                            if new_path.endswith(k['name']):
                                break
                        else:
                            endpath = new_path[len(xpath):]
                            new_path = xpath + pathname + endpath

            return new_path

        return "/" + "/".join(path_nodes)

    def get_allowed_ops(self, stmt, data):
        """No self.tree being built so override."""
        pass
