"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.1.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import delphix.api.gateway
from delphix.api.gateway.model.always_allowed_permission import AlwaysAllowedPermission
from delphix.api.gateway.model.scope_tag import ScopeTag
from delphix.api.gateway.model.scoped_object_item import ScopedObjectItem
globals()['AlwaysAllowedPermission'] = AlwaysAllowedPermission
globals()['ScopeTag'] = ScopeTag
globals()['ScopedObjectItem'] = ScopedObjectItem
from delphix.api.gateway.model.access_group_scope import AccessGroupScope


class TestAccessGroupScope(unittest.TestCase):
    """AccessGroupScope unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAccessGroupScope(self):
        """Test AccessGroupScope"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AccessGroupScope()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
