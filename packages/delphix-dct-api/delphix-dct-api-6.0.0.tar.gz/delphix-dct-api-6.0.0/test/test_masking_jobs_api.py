"""
    Delphix DCT API

    Delphix DCT API  # noqa: E501

    The version of the OpenAPI document: 3.1.0
    Contact: support@delphix.com
    Generated by: https://openapi-generator.tech
"""


import unittest

import delphix.api.gateway
from delphix.api.gateway.api.masking_jobs_api import MaskingJobsApi  # noqa: E501


class TestMaskingJobsApi(unittest.TestCase):
    """MaskingJobsApi unit test stubs"""

    def setUp(self):
        self.api = MaskingJobsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_copy_masking_job(self):
        """Test case for copy_masking_job

        Copies the masking job to another engine.  # noqa: E501
        """
        pass

    def test_create_masking_job_tag(self):
        """Test case for create_masking_job_tag

        Create tags for a Masking Job.  # noqa: E501
        """
        pass

    def test_delete_masking_job(self):
        """Test case for delete_masking_job

        Delete a masking job.  # noqa: E501
        """
        pass

    def test_delete_masking_job_tag(self):
        """Test case for delete_masking_job_tag

        Delete tags for a Masking Job.  # noqa: E501
        """
        pass

    def test_execute_masking_job(self):
        """Test case for execute_masking_job

        Execute a MaskingJob.  # noqa: E501
        """
        pass

    def test_get_masking_job_by_id(self):
        """Test case for get_masking_job_by_id

        Retrieve a MaskingJob by ID.  # noqa: E501
        """
        pass

    def test_get_masking_job_connectors(self):
        """Test case for get_masking_job_connectors

        Get connectors for a Masking Job by ID.  # noqa: E501
        """
        pass

    def test_get_masking_job_source_engines(self):
        """Test case for get_masking_job_source_engines

        Retrieve the list of masking jobs along with their source engine.  # noqa: E501
        """
        pass

    def test_get_masking_job_tag(self):
        """Test case for get_masking_job_tag

        Get tags for a Masking Job.  # noqa: E501
        """
        pass

    def test_get_masking_jobs(self):
        """Test case for get_masking_jobs

        Retrieve the list of masking jobs.  # noqa: E501
        """
        pass

    def test_migrate_masking_job(self):
        """Test case for migrate_masking_job

        Migrates the masking job from its current source engine to another engine.  # noqa: E501
        """
        pass

    def test_search_masking_job_source_engines(self):
        """Test case for search_masking_job_source_engines

        Search the list of masking jobs along with their source engine.  # noqa: E501
        """
        pass

    def test_search_masking_jobs(self):
        """Test case for search_masking_jobs

        Search masking jobs.  # noqa: E501
        """
        pass

    def test_update_masking_job_by_id(self):
        """Test case for update_masking_job_by_id

        Update values of a MaskingJob.  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
