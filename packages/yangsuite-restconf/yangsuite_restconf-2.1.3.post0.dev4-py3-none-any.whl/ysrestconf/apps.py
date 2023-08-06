# Copyright 2016 to 2021, Cisco Systems, Inc., all rights reserved.
try:
    from yangsuite.apps import YSAppConfig
except Exception:
    from django.apps import AppConfig as YSAppConfig


class YSrestconfConfig(YSAppConfig):
    name = 'ysrestconf'
    """str: Python module name (mandatory)."""

    url_prefix = 'restconf'
    """str: Prefix under which to include this module's URLs."""

    verbose_name = (
        'RESTCONF messaging presented in OpenAPI formt (Swagger) to RESTCONF'
        'enabled devices.'
    )

    menus = {
        'Protocols': [
            ('RESTCONF', ''),
        ],
    }
    """dict: Menu items ``{'menu': [(text, relative_url), ...], ...}``"""

    help_pages = [
        ('YANG Suite RESTCONF', 'restconf.html'),
    ]
