"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.1.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.environments_api import EnvironmentsApi  # noqa: E501


class TestEnvironmentsApi(unittest.TestCase):
    """EnvironmentsApi unit test stubs"""

    def setUp(self):
        self.api = EnvironmentsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_environment(self):
        """Test case for create_environment

        Create an environment.  # noqa: E501
        """
        pass

    def test_create_environment_tags(self):
        """Test case for create_environment_tags

        Create tags for an Environment.  # noqa: E501
        """
        pass

    def test_create_environment_user(self):
        """Test case for create_environment_user

        Create environment user.  # noqa: E501
        """
        pass

    def test_create_host(self):
        """Test case for create_host

        Create a new Host.  # noqa: E501
        """
        pass

    def test_delete_environment(self):
        """Test case for delete_environment

        Delete an environment by ID.  # noqa: E501
        """
        pass

    def test_delete_environment_tags(self):
        """Test case for delete_environment_tags

        Delete tags for an Environment.  # noqa: E501
        """
        pass

    def test_delete_environment_user(self):
        """Test case for delete_environment_user

        Delete environment user.  # noqa: E501
        """
        pass

    def test_delete_host(self):
        """Test case for delete_host

        Delete a Host.  # noqa: E501
        """
        pass

    def test_disable_environment(self):
        """Test case for disable_environment

        Disable environment.  # noqa: E501
        """
        pass

    def test_enable_environment(self):
        """Test case for enable_environment

        Enable a disabled environment.  # noqa: E501
        """
        pass

    def test_get_environment_by_id(self):
        """Test case for get_environment_by_id

        Returns an environment by ID.  # noqa: E501
        """
        pass

    def test_get_environments(self):
        """Test case for get_environments

        List all environments.  # noqa: E501
        """
        pass

    def test_get_tags_environment(self):
        """Test case for get_tags_environment

        Get tags for an Environment.  # noqa: E501
        """
        pass

    def test_list_environment_users(self):
        """Test case for list_environment_users

        List environment users.  # noqa: E501
        """
        pass

    def test_primary_environment_user(self):
        """Test case for primary_environment_user

        Set primary environment user.  # noqa: E501
        """
        pass

    def test_refresh_environment(self):
        """Test case for refresh_environment

        Refresh environment.  # noqa: E501
        """
        pass

    def test_search_environments(self):
        """Test case for search_environments

        Search for environments.  # noqa: E501
        """
        pass

    def test_snapshot_compatible_repositories(self):
        """Test case for snapshot_compatible_repositories

        Get compatible repositories corresponding to the snapshot.  # noqa: E501
        """
        pass

    def test_update_environment(self):
        """Test case for update_environment

        Update an environment by ID.  # noqa: E501
        """
        pass

    def test_update_environment_user(self):
        """Test case for update_environment_user

        Update environment user.  # noqa: E501
        """
        pass

    def test_update_host(self):
        """Test case for update_host

        Update a Host.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
