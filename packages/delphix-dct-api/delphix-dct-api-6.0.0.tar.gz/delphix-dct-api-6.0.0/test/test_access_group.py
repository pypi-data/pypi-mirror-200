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
from delphix.api.gateway.model.access_group_scope import AccessGroupScope
from delphix.api.gateway.model.tag import Tag
globals()['AccessGroupScope'] = AccessGroupScope
globals()['Tag'] = Tag
from delphix.api.gateway.model.access_group import AccessGroup


class TestAccessGroup(unittest.TestCase):
    """AccessGroup unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAccessGroup(self):
        """Test AccessGroup"""
        # FIXME: construct object with mandatory attributes with example values
        # model = AccessGroup()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
