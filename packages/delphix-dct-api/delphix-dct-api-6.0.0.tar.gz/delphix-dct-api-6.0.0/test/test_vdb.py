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
from delphix.api.gateway.model.additional_mount_point import AdditionalMountPoint
from delphix.api.gateway.model.tag import Tag
from delphix.api.gateway.model.virtual_dataset_hooks import VirtualDatasetHooks
globals()['AdditionalMountPoint'] = AdditionalMountPoint
globals()['Tag'] = Tag
globals()['VirtualDatasetHooks'] = VirtualDatasetHooks
from delphix.api.gateway.model.vdb import VDB


class TestVDB(unittest.TestCase):
    """VDB unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testVDB(self):
        """Test VDB"""
        # FIXME: construct object with mandatory attributes with example values
        # model = VDB()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
