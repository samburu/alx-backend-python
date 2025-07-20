#!/usr/bin/env python3
"""
Unit tests for  the module client.py.
"""
import unittest
from unittest.mock import PropertyMock, patch

from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient.org property."""

    @parameterized.expand(
        [
            ("google",),
            ("abc",),
        ]
    )
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data and
        calls get_json once with the correct URL."""
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        result = client.org  # property call triggers get_json internally

        expected_url = GithubOrgClient.ORG_URL.format(org=org_name)

        # Assert get_json called once with correct URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert the returned org value is the mocked response
        self.assertEqual(result, {"org": org_name})

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns correct repos_url from org payload
        """
        mock_org.return_value = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        client = GithubOrgClient("testorg")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/testorg/repos")
        mock_org.assert_called_once()
