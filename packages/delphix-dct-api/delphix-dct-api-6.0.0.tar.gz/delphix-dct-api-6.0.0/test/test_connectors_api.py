"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.1.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.connectors_api import ConnectorsApi  # noqa: E501


class TestConnectorsApi(unittest.TestCase):
    """ConnectorsApi unit test stubs"""

    def setUp(self):
        self.api = ConnectorsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_connectors_test(self):
        """Test case for connectors_test

        Checks connectivity between a masking engine and a remote data source.  # noqa: E501
        """
        pass

    def test_create_connector_tags(self):
        """Test case for create_connector_tags

        Create tags for a Connector.  # noqa: E501
        """
        pass

    def test_delete_connector_tag(self):
        """Test case for delete_connector_tag

        Delete tags for a Connector.  # noqa: E501
        """
        pass

    def test_get_connector_by_id(self):
        """Test case for get_connector_by_id

        Retrieve a masking Connector by ID.  # noqa: E501
        """
        pass

    def test_get_connector_tags(self):
        """Test case for get_connector_tags

        Get tags for a Connector.  # noqa: E501
        """
        pass

    def test_get_connectors(self):
        """Test case for get_connectors

        Retrieve the list of masking connectors.  # noqa: E501
        """
        pass

    def test_search_connectors(self):
        """Test case for search_connectors

        Search for masking Connectors.  # noqa: E501
        """
        pass

    def test_update_connector_by_id(self):
        """Test case for update_connector_by_id

        Update a masking Connector by ID.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
