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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Unit-test for GithubOrgClient.public_repos
        """
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns expected boolean"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
